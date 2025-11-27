# services/media_service/repository.py
from collections.abc import Sequence

from sqlalchemy import select

from db.models.media import Media
from db.repository.base import BaseRepository


class MediaRepository(BaseRepository):
    """
    Репозиторий для работы с медиа-файлами постов.
    """

    async def create_for_post(self, post_id: int, url: str) -> Media:
        """
        Создать медиа-запись для поста.
        """
        return await self.save(
            Media,
            values={
                "post_id": post_id,
                "url": url,
            },
        )

    async def list_for_post(self, post_id: int) -> Sequence[Media]:
        """
        Получить все медиа для поста.
        """
        result = await self.session.scalars(select(Media).where(Media.post_id == post_id))
        return result.all()

    async def delete(self, media_id: int) -> None:
        """
        Удалить медиа-запись.
        """
        media = await self.session.get(Media, media_id)
        if media:
            await self.session.delete(media)
