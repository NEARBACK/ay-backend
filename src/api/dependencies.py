from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from core.app_state import AppState
from services.dummy_service.repository import DummyRepository
from services.dummy_service.service import DummyService


async def get_state(request: Request) -> AppState:
    return request.state.app_state


StateDependency = Annotated[AppState, Depends(get_state)]


async def get_engine(state: StateDependency) -> AsyncEngine:
    return state.engine


async def get_http_client(state: StateDependency) -> AsyncClient:
    return state.http_client


async def get_session(
    engine: AsyncEngine = Depends(get_engine),
) -> AsyncGenerator[AsyncSession, None]:
    session_local = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
    async with session_local() as session:
        yield session


async def get_dummy_service(session: AsyncSession = Depends(get_session)) -> DummyService:
    return DummyService(DummyRepository(session))
