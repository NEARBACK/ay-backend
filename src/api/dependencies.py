from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Header, Request
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from core.app_state import AppState
from db.models.user import Users
from schemas.user import UserCreate
from services.donation_service.repository import DonationRepository
from services.donation_service.service import DonationService
from services.dummy_service.repository import DummyRepository
from services.dummy_service.service import DummyService
from services.media_service.repository import MediaRepository
from services.media_service.service import MediaService
from services.post_service.repository import PostRepository
from services.post_service.service import PostService
from services.user_service.repository import UserRepository
from services.user_service.service import UserService


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


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))


async def get_post_service(session: AsyncSession = Depends(get_session)) -> PostService:
    return PostService(PostRepository(session))


async def get_donation_service(
    session: AsyncSession = Depends(get_session),
) -> DonationService:
    donation_repo = DonationRepository(session)
    post_repo = PostRepository(session)
    return DonationService(donation_repo=donation_repo, post_repo=post_repo)


async def get_current_user(
    wallet_address: str = Header(..., alias="X-Wallet-Address"),
    user_service: UserService = Depends(get_user_service),
) -> Users:
    """
    Простейшая "авторизация":
    - фронт передаёт в каждом запросе X-Wallet-Address: <TON-адрес>
    - мы ищем/создаём пользователя в БД.
    """
    user = await user_service.get_by_wallet(wallet_address)
    if user:
        return user

    # лениво создаём юзера, если не найден
    created = await user_service.get_or_create_user(UserCreate(wallet_address=wallet_address, display_name=None))
    return created


async def get_media_service(
    session: AsyncSession = Depends(get_session),
) -> MediaService:
    repo = MediaRepository(session)
    return MediaService(repo)
