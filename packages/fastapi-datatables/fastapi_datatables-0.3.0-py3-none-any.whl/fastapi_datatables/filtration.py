from __future__ import annotations

from typing import Optional, Literal, Union, TypedDict, Any
from .operations import FiltrationOperator
from pydantic import BaseModel, validator
from sqlalchemy.orm import Query
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
from .table import DataTable


class FilterSpec(TypedDict):
    model: Optional[str]
    field: str
    op: str
    value: str


class RawFilterSpec(TypedDict):
    field: str
    op: Union[FiltrationOperator, str]
    value: str


AnyFilterSpec = Union[RawFilterSpec, FilterSpec]


class SortSpec(TypedDict):
    field: str
    direction: str


class ModelSortSpec(SortSpec):
    model: str


class ParsingData:
    _or: list[FilterSpec]
    _and: list[FilterSpec]

    def __init__(
        self,
        json: dict[str, FilterSpec] = {},
        *,
        _or: Union[list[RawFilterSpec], list[FilterSpec]] = [],  # type: ignore
        _and: Union[list[RawFilterSpec], list[FilterSpec]] = [],  # type: ignore
    ) -> None:
        self._or = json.get("or", []) + [ParsingData.__convert_raw(e) for e in _or]  # type: ignore
        self._and = json.get("and", []) + [ParsingData.__convert_raw(e) for e in _and]  # type: ignore

    def to_spec(self) -> dict[str, list[FilterSpec]]:
        res: dict[str, list[FilterSpec]] = {}
        if self._or != []:
            res |= {"or": self._or}
        if self._and != []:
            res |= {"and": self._and}
        return res

    @staticmethod
    def __split_field(field: str) -> dict[str, str]:
        # The field can name the model explicitly like
        # Model.field
        # Otherways the default main model will be used
        if "." in field:
            if field.count(".") > 1:
                raise ValueError("In field can only be one `.`")

            table, field = field.split(".")
            return {"model": table, "field": field}
        else:
            return {"field": field}

    @staticmethod
    def __convert_raw(raw: AnyFilterSpec) -> FilterSpec:
        op = raw["op"]
        if isinstance(op, FiltrationOperator):
            op = str(op.value)

        if "model" in raw:
            return {
                "model": raw["model"],  # type: ignore
                "field": raw["field"],
                "op": op,
                "value": raw["value"],
            }
        else:
            return ParsingData.__split_field(raw["field"]) | {  # type: ignore
                "op": op,
                "value": raw["value"],
            }

    def copy(self) -> ParsingData:
        """ Return the shallow copy of ParsingData object. """

        return ParsingData(_or=self._or.copy(), _and=self._and.copy())

    @staticmethod
    def from_dict(data: FilterSpec) -> ParsingData:
        return ParsingData(_and=[data])

    @staticmethod
    def disjunction(data: list[FilterSpec] = []) -> ParsingData:
        """ Construct ParsingData using a logical or. """
        return ParsingData(_or=data)

    @staticmethod
    def conjunction(data: list[FilterSpec] = []) -> ParsingData:
        """ Construct ParsingData using a logical and. """
        return ParsingData(_and=data)

    @staticmethod
    def __get_spec_field(spec: FilterSpec) -> str:
        return f"{spec['model']}.{spec['field']}" if "model" in spec else spec["field"]

    def __add__(self, other: Union[ParsingData, FilterSpec]) -> ParsingData:
        if isinstance(other, dict):
            other = ParsingData.from_dict(other)
        result = self.copy()
        result._and.extend(other._and)
        result._or.extend(other._or)
        return result

    def __getitem__(self, key: str) -> set[tuple[FiltrationOperator, str]]:
        return {
            (FiltrationOperator(spec["op"]), spec["value"])
            for spec in self._and
            if self.__get_spec_field(spec) == key
        }

    def __contains__(self, item: str) -> bool:
        return any(item == self.__get_spec_field(spec) for spec in self._and)


class FiltrationData(BaseModel):
    to_filter: ParsingData = ParsingData()
    page_number: int = 1
    page_size: int = 10
    order_by: Optional[str] = None
    sort_by: Literal["asc", "desc"] = "asc"

    class Config:
        arbitrary_types_allowed = True

    def __get_sort_spec(self) -> list[ModelSortSpec]:
        return [self.__split_field(self.order_by) | {"direction": self.sort_by}]  # type: ignore

    def apply(self, query: Query) -> DataTable:
        filter_spec = self.to_filter.to_spec()
        query = apply_filters(query, filter_spec)

        if self.order_by is not None:
            sort_spec = self.__get_sort_spec()
            query = apply_sort(query, sort_spec)

        query, pagination = apply_pagination(
            query, page_number=self.page_number, page_size=self.page_size
        )
        page_size, page_number, num_pages, total_results = pagination

        return DataTable(
            page_size=page_size,
            page_number=page_number,
            num_pages=num_pages,
            total_results=total_results,
            items=query.all(),
        )

    def filter(
        self,
        field: str,
        value: str,
        operator: Union[FiltrationOperator, str] = FiltrationOperator.EQUAL,
    ) -> FiltrationData:
        if isinstance(operator, str):
            operator = FiltrationOperator(operator)

        self.to_filter += {
            "field": field,
            "value": value,
            "op": operator,
        }
        return self
