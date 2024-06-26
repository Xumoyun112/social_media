from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


# post
class PostOutput(BaseModel):
    id: int
    title: str
    content: str
    created: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str


class LikeSchama(BaseModel):
    post_id: int


class CommentSchema(BaseModel):
    post_id: int
    content: str


class PostDetail(PostCreate):
    id: int
    comments: list[CommentSchema]
    # user: UserOutput


class FollowersShema(BaseModel):
    id: int
    user: list[UserOutput]


class AllFollowerShema(BaseModel):
    id: int
    follower: UserOutput
    is_following: bool


class AllFollowingShema(BaseModel):
    id: int
    following: UserOutput
    is_following: bool


class RoomCreate(BaseModel):
    name: str


class RoomOutput(RoomCreate):
    id: int
    created: datetime
