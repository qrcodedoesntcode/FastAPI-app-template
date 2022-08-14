from typing import Generic, TypeVar

from fastapi import Query
from fastapi_pagination.default import Page as BasePage
from fastapi_pagination.default import Params as BaseParams

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(100, ge=1, le=200, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
