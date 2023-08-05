from __future__ import annotations

from typing import Optional, Literal, Union, TypedDict
from .operations import FiltrationOperator
from pydantic import BaseModel
from sqlalchemy.orm import Query
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
from .table import DataTable

ParsingData = dict[str, list[tuple[FiltrationOperator, str]]]


class FilterSpec(TypedDict):
    field: str
    op: str
    value: str


class ModelFilterSpec(FilterSpec):
    model: str


class FieldSplit(TypedDict):
    model: str
    field: str


class FieldUnsplit(TypedDict):
    field: str


class SortSpec(TypedDict):
    field: str
    direction: str


class ModelSortSpec(SortSpec):
    model: str


class FiltrationData(BaseModel):
    to_filter: ParsingData = {}
    page_number: int = 1
    page_size: int = 10
    order_by: Optional[str] = None
    sort_by: Literal["asc", "desc"] = "asc"

    def __split_field(self, field: str) -> Union[FieldSplit, FieldUnsplit]:
        # The field can name the model explicitly like
        # Model.field
        # Otherways the default main model will be used
        if "." in field:
            if field.count(".") > 1:
                raise ValueError("In field can only be one `.`")

            table, field = field.split(".")
            return {"model": table, "field": field}
        else:
            return {
                "field": field,
            }

    def __filter_to_spec(
        self, field: str, operator: FiltrationOperator, value: str
    ) -> Union[FilterSpec, ModelFilterSpec]:
        return self.__split_field(field) | {  # type: ignore
            "op": operator.value,
            "value": value,
        }

    def __get_sort_spec(self) -> list[ModelSortSpec]:
        return [self.__split_field(self.order_by) | {"direction": self.sort_by}]  # type: ignore

    def apply(self, query: Query) -> DataTable:
        filter_spec = [
            self.__filter_to_spec(field, operator, value)
            for field, filters in self.to_filter.items()
            for operator, value in filters
        ]
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

        if field not in self.to_filter:
            self.to_filter[field] = []

        self.to_filter[field].append((operator, value))
        return self
