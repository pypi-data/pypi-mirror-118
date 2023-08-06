from ipaddress import IPv4Address, IPv6Address
from typing import Union

from pydantic import BaseModel

IPAddress = Union[IPv4Address, IPv6Address]

class ConditionRequestIP(BaseModel):
    in_: list[IPAddress]
    not_in: list[IPAddress]

class Condition(BaseModel):
    request_in: ConditionRequestIP