from datetime import datetime

from pydantic import Field, RootModel

from .base import BaseSchema


class DonationSchema(BaseSchema):
    """
    DTO для модели Donations.
    """

    id: int = Field(title="ID", examples=[1])
    post_id: int = Field(title="Post ID", examples=[1])
    from_wallet: str = Field(title="From wallet", examples=["EQB_from..."])
    to_wallet: str = Field(title="To wallet", examples=["EQB_to..."])
    amount_nanoton: int = Field(
        title="Amount in nanoton",
        examples=[100_000_000],
    )
    status: str = Field(
        title="Status",
        examples=["PENDING", "CONFIRMED", "FAILED"],
    )
    tx_hash: str | None = Field(
        default=None,
        title="Transaction hash",
        examples=["SOME_TON_TX_HASH"],
    )
    comment: str | None = Field(
        default=None,
        title="Comment",
        examples=["donation:123"],
    )
    created_at: datetime = Field(
        title="Creation time",
        examples=["2025-11-24T12:00:00Z"],
    )
    updated_at: datetime = Field(
        title="Update time",
        examples=["2025-11-24T12:05:00Z"],
    )


DonationList = RootModel[list[DonationSchema]]


class DonationCreate(BaseSchema):
    """
    DTO для создания доната (инициация).
    """

    amount_nanoton: int = Field(
        title="Amount in nanoton",
        gt=0,
        examples=[100_000_000],
    )


class DonationConfirm(BaseSchema):
    """
    DTO для подтверждения доната после Tonkeeper.
    """

    tx_hash: str = Field(
        title="Transaction hash from TON",
        examples=["SOME_TON_TX_HASH"],
    )
