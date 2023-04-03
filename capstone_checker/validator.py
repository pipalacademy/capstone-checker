from typing import Any

from pydantic import BaseModel


class CheckModel(BaseModel):
    title: str
    name: str
    args: dict[str, Any]


class TaskModel(BaseModel):
    name: str
    title: str
    description: str
    checks: list[CheckModel]


class ProjectModel(BaseModel):
    name: str
    title: str
    short_description: str
    description: str
    tags: list[str]
    is_published: bool | None = None
    tasks: list[TaskModel]
