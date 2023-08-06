from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from cf_cli.backend.schemas.utils import identifier
from cf_cli.backend.schemas.organization import Organization

class User(BaseModel):
    id_: identifier
    email: Annotated[str, Field(max_length=90)]
    first_name: Optional[Annotated[str, Field(max_length=60)]]
    last_name: Optional[Annotated[str, Field(max_length=60)]]
    username: Annotated[str, Field(min_length=3, max_length=90, regex=r"^[a-z0-9]+([\-\._]?[a-z0-9]+)+$")]
    telephone: Optional[Annotated[str, Field(max_length=20)]]
    country: Optional[Annotated[str, Field(max_length=30)]]
    zipcode: Optional[Annotated[str, Field(max_length=20)]]
    created_on: datetime
    modified_on: datetime
    two_factor_authentication_enabled: bool
    suspended: bool
    organizations: list[Organization]
    betas: Optional[list[str]]
    has_pro_zones: bool
    has_business_zones: bool
    has_enterprise_zones: bool