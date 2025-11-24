from importlib.metadata import version
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from src.api.dependencies import StateDependency, get_engine

infra_router = APIRouter()


class VersionResponse(BaseModel):
    version: str


@infra_router.get("/status", response_class=JSONResponse)
async def get_system_status(engine: Annotated[AsyncEngine, Depends(get_engine)]) -> JSONResponse:
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    return JSONResponse(content={})


@infra_router.get("/version", summary="Проверить версию приложения")
async def get_version(state: StateDependency) -> VersionResponse:
    return VersionResponse(version=version(state.settings.app_name))
