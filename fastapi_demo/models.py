from typing import Optional
from pydantic import BaseModel, ValidationError
from enum import IntEnum


class RoleEnum(IntEnum):
    admin = 1
    moderator = 2
    user = 3

class User(BaseModel):
    id: int = 0
    role: RoleEnum = RoleEnum.user
    username: str
    email: str
