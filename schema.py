from typing import List, Union

from pydantic import BaseModel


class CommonBaseModel(BaseModel):
    class Config:
        orm_mode = True


class BlogSchema(CommonBaseModel):
    title: str
    body: str


class UserResponse(CommonBaseModel):
    name: str
    email: str


class ShowBlog(CommonBaseModel):
    title: str
    body: str
    creator: UserResponse


class User(CommonBaseModel):
    name: str
    email: str
    password: str


class Login(CommonBaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None