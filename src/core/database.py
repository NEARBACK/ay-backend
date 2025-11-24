from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.settings import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        url=settings.postgres_url,
        pool_size=settings.pool_max_size,
        echo=settings.postgres_echo,
    )
