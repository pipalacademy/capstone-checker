from typing import Any

from pydantic import BaseModel, Field, root_validator, validator


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
    project_type: str
    deployment_type: str
    deployment_options: dict[str, Any] = Field(default_factory=dict)
    tasks: list[TaskModel]

    @root_validator(pre=True)
    def split_deployment_type_into_key_and_options(cls, values):
        if "deployment_type" not in values:
            # default validation will catch this
            return values

        deployment_type = values["deployment_type"]
        if isinstance(deployment_type, dict):
            deployment_type_items = list(deployment_type.items())
            if len(deployment_type_items) != 1:
                raise ValueError(
                    "deployment_type must either be a string or a dict with only one key"
                )

            deployment_type, deployment_options = deployment_type_items[0]
            return dict(
                values, deployment_type=deployment_type, deployment_options=deployment_options
            )
        else:
            return values

    @root_validator
    def validate_options_for_custom_deployment(cls, values):
        depl_type, depl_opts = values["deployment_type"], values["deployment_options"]
        if depl_type == "custom" and "url" not in depl_opts:
            raise ValueError("url is required for custom deployment")
        else:
            return values

    @validator("deployment_type")
    def validate_deployment_type(cls, v):
        if v not in {"custom", "nomad"}:
            raise ValueError("deployment_type must be either 'custom' or 'nomad'")
        else:
            return v
