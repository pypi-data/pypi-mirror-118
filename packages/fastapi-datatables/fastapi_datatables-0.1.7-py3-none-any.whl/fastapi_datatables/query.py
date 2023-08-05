from __future__ import annotations
from functools import cache

from typing import Callable, Iterable, Union, Literal, Optional, overload
from fastapi import Request, HTTPException, Query
from starlette.datastructures import QueryParams
from abc import ABC, abstractmethod
from .operations import FiltrationOperator
from .filtration import FiltrationData

import inspect
from functools import singledispatch


class QueryParsingException(HTTPException):
    """An exception that is raised when a filtration query if mallformed."""


ParsingData = dict[str, list[tuple[FiltrationOperator, str]]]


class QueryParser(ABC):
    """A base object to handle parsing the request query for filtration."""

    def __init__(
        self,
        valid_columns: list[str],
        *,
        default_operator_factory: Callable[[str], FiltrationOperator],
        available_operators_factory: Callable[[str], list[FiltrationOperator]],
    ) -> None:
        self._valid_columns = valid_columns
        self._default_operator_factory = default_operator_factory
        self._available_operators_factory = available_operators_factory

        for column in valid_columns:
            default_op = default_operator_factory(column)
            available_ops = available_operators_factory(column)
            if default_op not in available_ops:
                raise ValueError(
                    f"For column {column} default operator is {default_op}, "
                    f"but it is not available. "
                    f"Available ones: {available_ops}"
                )

    def parse(self, query_params: QueryParams) -> ParsingData:
        """Parse the query and get all fields that are in `valid_columns`."""

        for _filter in self._valid_columns:
            if _filter in FiltrationData().dict():
                raise RuntimeError(
                    f"{_filter!r} is a reserved keyword, can not use it for filtration"
                )

        result: ParsingData = {}
        for key, value in query_params.multi_items():
            if self._verify_present(key):
                result = QueryParser.__combine_parse_dicts(
                    result, self._process_pair(key, value)
                )
        return result

    @abstractmethod
    def _process_pair(self, key: str, value: str) -> ParsingData:
        """Parse and validate the key-value pair from query."""

    @abstractmethod
    def _verify_present(self, key: str) -> bool:
        """Verify, if the `key` should be present in filtration from `to_filter`."""

    @abstractmethod
    def modify_signature(self, func: Callable) -> Callable:
        """Modify a function signature to fix OpenAPI params."""

    @staticmethod
    def __combine_parse_dicts(first: ParsingData, other: ParsingData) -> ParsingData:
        result = first.copy()
        for k, v in other.items():
            if k in result:
                result[k].extend(v)
            else:
                result[k] = v
        return ParsingData(result)


class LHSQueryParser(QueryParser):
    """
    A Left Hand Side parser, works with passing filtration keys in key format:

    `?item[gte]=11&item[lte]=20`
    """

    def _process_pair(self, key: str, value: str) -> ParsingData:
        # If a key contains square brackets
        if any(sym in key for sym in "[]"):
            # More then 1 of each bracket
            if key.count("[") != 1 or key.count("]") != 1:
                raise QueryParsingException(
                    400,
                    detail="Filtration square brackets should contain "
                    f"exactly one left and one right square bracket, but got {key!r} ",
                )

            # Order is messed up
            left_bracket_index = key.index("[")
            right_bracket_index = key.index("]")
            if left_bracket_index > right_bracket_index:
                raise QueryParsingException(
                    400,
                    detail="Filtration square brackets should start with `[` "
                    f"and end with `]`, but got {key!r} ",
                )

            # From format f"{key_data}[{key_filter}]"
            key_filter_str = key[left_bracket_index + 1 : right_bracket_index]
            key_data = key[:left_bracket_index]

            available_operators = self._available_operators_factory(key_data)
            filtrations_possible_str = ", ".join(
                f"{filtration_operator.value!r}"
                for filtration_operator in available_operators
            )

            # Convert to available Filtration Operators
            try:
                key_filter = FiltrationOperator(key_filter_str)
            except ValueError as e:
                raise QueryParsingException(
                    422,
                    detail=f"Invalid filter key: {key_filter_str!r}. "
                    f"Available ones: {filtrations_possible_str}",
                ) from e

            # Verify if the filter can be used
            if key_filter not in available_operators:
                raise QueryParsingException(
                    422,
                    detail=f"Filter not available: {key_filter.value!r}. "
                    f"Available ones: {filtrations_possible_str}",
                )

            return {key_data: [(key_filter, value)]}

        # Otherwise it will be considered an equality filter
        else:
            return {key: [(self._default_operator_factory(key), value)]}

    def _verify_present(self, key: str) -> bool:
        return key.split("[")[0] in self._valid_columns

    def modify_signature(self, func: Callable) -> Callable:
        old_signature = inspect.signature(func)
        old_parameters = list(old_signature.parameters.values())
        new_parameters = [
            x
            for x in old_parameters
            if x.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]

        for col in self._valid_columns:
            available_operators = self._available_operators_factory(col)
            default_operator = self._default_operator_factory(col)
            available_operators_str = (
                ", ".join(f"`{op.value}`" for op in available_operators)
                if set(available_operators) != set(FiltrationOperator)
                else "`*`"
            )

            param = inspect.Parameter(
                name=col.replace(".", "_"),
                kind=inspect.Parameter.KEYWORD_ONLY,
                annotation=Optional[str],
                default=Query(
                    None,
                    alias=f"{col}[<FilterOperator>]",
                    title=f"Filtering by {col!r} column",
                    description="\n\n".join(
                        [
                            f"Available operators: {available_operators_str}",
                            f"Default operator: `{default_operator.value}`",
                        ]
                    ),
                ),
            )
            new_parameters.append(param)

        new_signature = old_signature.replace(parameters=new_parameters)
        setattr(func, "__signature__", new_signature)
        return func


AnyFiltrationOperator = Union[FiltrationOperator, str]


def get_filtration(
    valid_columns: Iterable[str],
    *,
    operator_data: Optional[
        dict[
            str,
            tuple[
                Optional[AnyFiltrationOperator], Optional[list[AnyFiltrationOperator]]
            ],
        ]
    ] = None,
) -> Callable[..., FiltrationData]:
    """
    Returns a function, that can be used in a Depends to get filtration data from query.
    """

    @cache
    def operator_factory(
        key: str,
    ) -> tuple[FiltrationOperator, list[FiltrationOperator]]:
        if operator_data is None or key not in operator_data:
            return (FiltrationOperator.EQUAL, list(FiltrationOperator))

        default, available = operator_data[key]
        if default is None:
            default = FiltrationOperator.EQUAL
        if available is None:
            available = list(FiltrationOperator)

        return FiltrationOperator(default), [FiltrationOperator(op) for op in available]

    parser = LHSQueryParser(
        valid_columns,
        default_operator_factory=lambda key: operator_factory(key)[0],
        available_operators_factory=lambda key: operator_factory(key)[1],
    )

    @parser.modify_signature
    def get_filtration_data(
        request: Request,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        sort_by: Literal["asc", "desc"] = "asc",
        **kwargs,
    ) -> FiltrationData:
        if order_by is not None and order_by not in valid_columns:
            raise HTTPException(
                422,
                detail=f"order_by = {order_by!r} is not a valid column. "
                f"Valid columns: {', '.join(valid_columns)}",
            )

        return FiltrationData(
            to_filter=parser.parse(request.query_params),
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort_by=sort_by,
        )

    return get_filtration_data
