from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from core.app_state import init_state, shutdown
from core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[Mapping[str, Any]]:
    state = init_state(settings)

    yield {"app_state": state}

    await shutdown(state)
