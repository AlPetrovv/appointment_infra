from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

T = TypeVar("T")
CustomPage = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(5, ge=1, le=100, alias="limit"),
        page=Query(1, ge=1, alias="offset"),
    ),
]
