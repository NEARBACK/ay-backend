from collections.abc import Sequence

from sqlalchemy import select

from db.models.dummy import Dummy
from db.repository.dummy import BaseRepository


class DummyRepository(BaseRepository):
    """
    Репозиторий для управления объектами Dummy.
    Содержит методы для работы с базой данных: создание/обновление/удаления и получение записей.
    """

    async def create_dummy(self, name: str) -> Dummy:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        return await self.save(Dummy, values={"name": name})

    async def get_all_dummies(self, limit: int = 100, offset: int = 0) -> Sequence[Dummy]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        result = await self.session.scalars(
            select(Dummy).limit(limit).offset(offset),
        )

        return result.all()

    async def filter(
        self,
        name: str | None = None,
    ) -> Sequence[Dummy]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = select(Dummy)
        if name:
            query = query.where(Dummy.name == name)
        rows = await self.session.scalars(query)
        return rows.all()
