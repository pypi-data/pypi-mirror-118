from typing import Annotated

from pydantic import Field

identifier = Annotated[str, Field(max_length=32)]