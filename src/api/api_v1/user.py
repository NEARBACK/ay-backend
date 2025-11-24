from http import HTTPStatus

from fastapi import APIRouter
from fastapi.param_functions import Depends

from db.models.user import Users
from schemas.user import User, UserCreate
from services.user_service.service import UserService
from src.api.dependencies import get_current_user, get_user_service

router = APIRouter()


@router.post(
    "/auth/ton-connect",
    summary="Авторизация через TON Connect (get_or_create по wallet)",
    status_code=HTTPStatus.OK,
)
async def auth_ton_connect(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    user = await user_service.get_or_create_user(payload)
    return User.model_validate(user)


@router.get("/me")
async def get_me(
    current_user: Users = Depends(get_current_user),
) -> User:
    return User.model_validate(current_user)
