# services/media_service/service.py
from collections.abc import Sequence

from db.models.media import Media
from services.media_service.repository import MediaRepository


class MediaService:
    """
    Сервис для работы с медиа.
    """

    def __init__(self, repository: MediaRepository):
        self.repository = repository

    async def attach_to_post(self, post_id: int, url: str) -> Media:
        """
        Привязать медиа (по URL) к посту.
        """
        async with self.repository.atomic():
            return await self.repository.create_for_post(post_id=post_id, url=url)

    async def list_for_post(self, post_id: int) -> Sequence[Media]:
        """
        Список медиа для поста.
        """
        return await self.repository.list_for_post(post_id)

    async def delete_media(self, media_id: int) -> None:
        """
        Удалить медиа.
        """
        async with self.repository.atomic():
            await self.repository.delete(media_id)
