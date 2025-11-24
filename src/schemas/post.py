from datetime import datetime

from pydantic import Field, RootModel

from .base import BaseSchema
from .user import User


class Post(BaseSchema):
    """
    DTO для модели Posts.
    """

    id: int = Field(title="ID", examples=[1])
    author_id: int = Field(title="Author ID", examples=[1])
    text: str = Field(title="Post text", examples=["My first TON post"])
    recommended_amount_nanoton: int = Field(
        title="Recommended donation in nanoton",
        examples=[100_000_000],
    )
    created_at: datetime = Field(
        title="Creation time",
        examples=["2025-11-24T12:00:00Z"],
    )


class PostWithAuthor(Post):
    """
    Пост вместе с данными автора для фронта.
    """

    author: User


PostList = RootModel[list[PostWithAuthor]]


class PostCreate(BaseSchema):
    """
    DTO создания поста.
    """

    text: str = Field(
        title="Post text",
        min_length=1,
        max_length=2000,
        examples=["Hello TON world!"],
    )
    recommended_amount_nanoton: int = Field(
        title="Recommended donation amount in nanoton",
        gt=0,
        examples=[100_000_000],
    )
