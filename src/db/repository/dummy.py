from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from typing import Any, TypeVar

from sqlalchemy import ColumnExpressionArgument, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.dummy import Dummy

T = TypeVar("T", bound=Dummy)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @asynccontextmanager
    async def atomic(self) -> AsyncGenerator[None, None]:
        async with self.session.begin_nested():
            yield

        if self.session.in_transaction() and not self.session.in_nested_transaction():
            await self.session.commit()

    async def save(self, model: type[T], values: dict[str, Any]) -> T:
        result = await self.session.scalar(insert(model).values(**values).returning(model))
        if not result:
            raise ValueError("Can't save object")
        return result

    async def bulk_insert(self, model: type[T], values: list[dict[str, Any]]) -> Sequence[T]:
        result = await self.session.scalars(insert(model).returning(model), values)
        return result.all()

    async def update(
        self,
        model: type[T],
        values: dict[str, Any],
        *,
        custom_filter: tuple[ColumnExpressionArgument[bool], ...] = (),
    ) -> Sequence[T]:
        result = await self.session.scalars(
            update(model).where(and_(True, *custom_filter)).values(**values).returning(model)
        )
        return result.all()

    async def update_by(
        self,
        model: type[T],
        values: dict[str, Any],
        *,
        custom_filter: tuple[ColumnExpressionArgument[bool], ...] = (),
    ) -> T | None:
        return await self.session.scalar(
            update(model).where(and_(True, *custom_filter)).values(**values).returning(model)
        )
