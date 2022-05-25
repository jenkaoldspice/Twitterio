from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr
from datetime import datetime


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    updated_at: datetime
    created_at: datetime


class UserCount(BaseModel):

    post_count: int


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("password don't match")
        return v
