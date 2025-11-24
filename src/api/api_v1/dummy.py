from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.param_functions import Depends

from schemas.dummy import Dummy, DummyCreate, DummyList
from services.dummy_service.service import DummyService
from src.api.dependencies import get_dummy_service

router = APIRouter()


@router.get("/", summary="Получить список объектов")
async def get_dummy_models(
    limit: Annotated[int, Query(description="Размер страницы")] = 10,
    page: Annotated[int, Query(description="Индекс страницы")] = 0,
    service: DummyService = Depends(get_dummy_service),
) -> DummyList:
    """
    Получить список объектов из базы данных.
    """
    result = await service.get_all_dummies(limit, page)
    return DummyList.model_validate(result)


@router.post("/", summary="Создать новый объект", status_code=HTTPStatus.CREATED)
async def create_dummy_model(
    new_dummy_object: DummyCreate,
    service: DummyService = Depends(get_dummy_service),
) -> Dummy:
    """
    Создать новый объект в базе данных.
    """
    result = await service.create_dummy(new_dummy_object)
    return Dummy.model_validate(result)
