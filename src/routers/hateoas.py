import math
from typing import Any, Self

from pydantic import BaseModel, model_validator


class HateoasModel(BaseModel):
    items: list
    page: int
    limit: int
    total_count: int
    path: str
    other_args: dict | None = None
    url: str | None = None
    links: dict[str, Any] | None = None

    @model_validator(mode="after")
    def get_url(self) -> Self:
        self.url = self.path
        return self

    @model_validator(mode="after")
    def get_links(self) -> Self:
        if not (pages := math.ceil(self.total_count / self.limit)):
            self.links = {}
            return self
        other_args = ""
        if self.other_args:
            for key, value in self.other_args.items():
                other_args += f"&{key}={value}" if value is not None else ""
        self.links = {
            "first": {"href": f"{self.url}?page=1&limit={self.limit}{other_args}"},
            "last": {"href": f"{self.url}?page={pages}&limit={self.limit}{other_args}"},
        }
        if self.page > 1:
            self.links["previous"] = {"href": f"{self.url}?page={self.page - 1}&limit={self.limit}{other_args}"}
        if self.page < pages:
            self.links["next"] = {"href": f"{self.url}?page={self.page + 1}&limit={self.limit}{other_args}"}
        return self
