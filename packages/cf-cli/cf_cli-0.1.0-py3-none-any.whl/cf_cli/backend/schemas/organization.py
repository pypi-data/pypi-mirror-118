from typing import Annotated, Literal

from pydantic import BaseModel, Field

from cf_cli.backend.schemas.utils import identifier


class Organization(BaseModel):
    id_: identifier
    name: Annotated[str, Field(max_length=100)]
    status: Literal["member", "invited"]
    permissions: list[Annotated[str, Field(max_length=160)]]
    roles: list[Annotated[str, Field(max_length=120)]]