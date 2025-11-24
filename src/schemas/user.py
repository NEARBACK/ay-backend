from datetime import datetime

from pydantic import Field, RootModel

from .base import BaseSchema


class User(BaseSchema):
    """
    DTO для модели Users.
    """

    id: int = Field(title="ID", examples=[1])
    wallet_address: str = Field(title="TON wallet address", examples=["EQBxxxxx"])
    display_name: str | None = Field(
        default=None,
        title="Display name",
        examples=["Nearback"],
    )
    created_at: datetime = Field(
        title="Creation time (ISO string or DB string)",
        examples=["2025-11-24T12:00:00Z"],
    )


UserList = RootModel[list[User]]


class UserCreate(BaseSchema):
    """
    DTO создания пользователя (обычно через TON connect).
    """

    wallet_address: str = Field(title="TON wallet address", examples=["EQBxxxxx"])
    display_name: str | None = Field(
        default=None,
        title="Display name",
        examples=["Nearback"],
    )
