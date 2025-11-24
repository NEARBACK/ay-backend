from collections.abc import Sequence

from db.models.dummy import Dummy
from schemas.dummy import DummyCreate
from services.dummy_service.repository import DummyRepository


class DummyService:
    """
    Сервис для работы с объектами Dummy.

    Отвечает за бизнес-логику создания и получения объектов,
    используя DummyRepository для взаимодействия с базой данных.
    """

    def __init__(self, repository: DummyRepository):
        self.repository = repository

    async def create_dummy(self, data: DummyCreate) -> Dummy:
        async with self.repository.atomic():
            return await self.repository.create_dummy(data.name)

    async def get_all_dummies(self, limit: int, offset: int) -> Sequence[Dummy]:
        return await self.repository.get_all_dummies(limit, offset)
