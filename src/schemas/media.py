# schemas/media.py
from pydantic import Field, RootModel

from .base import BaseSchema


class Media(BaseSchema):
    """
    DTO для модели Media.
    """

    id: int = Field(title="ID", examples=[1])
    post_id: int = Field(title="Post ID", examples=[1])
    url: str = Field(
        title="Media URL",
        examples=["https://example.com/image.jpg"],
    )


class MediaCreate(BaseSchema):
    """
    DTO для создания медиа-записи.
    Сейчас — просто URL картинки.
    Потом можно заменить на UploadFile.
    """

    url: str = Field(
        title="Media URL",
        min_length=1,
        max_length=700,
        examples=["https://example.com/image.jpg"],
    )


MediaList = RootModel[list[Media]]
