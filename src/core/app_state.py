from dataclasses import dataclass

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from core.database import create_engine
from core.settings import Settings


@dataclass
class AppState:
    engine: AsyncEngine
    settings: Settings
    http_client: AsyncClient


def init_state(config: Settings) -> AppState:
    engine = create_engine(config)

    state = AppState(
        engine=engine,
        settings=config,
        http_client=AsyncClient(base_url="some-exteranal-url"),
    )
    return state


async def shutdown(app_state: AppState) -> None:
    await app_state.engine.dispose()
    await app_state.http_client.aclose()
