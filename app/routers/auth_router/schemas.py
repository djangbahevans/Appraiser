from typing import Optional

from pydantic import BaseModel

from ..user_router.schemas import User, UserBase


class Auth(UserBase):
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: Optional[str]
    refresh_token: Optional[str]
