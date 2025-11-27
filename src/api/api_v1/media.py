from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from db.models.post import Posts
from schemas.media import Media, MediaCreate, MediaList
from services.media_service.service import MediaService
from services.post_service.service import PostService
from src.api.dependencies import get_media_service, get_post_service

router = APIRouter()

MediaServiceDep = Annotated[MediaService, Depends(get_media_service)]
PostServiceDep = Annotated[PostService, Depends(get_post_service)]


@router.post(
    "/posts/{post_id}/media",
    summary="Добавить медиа к посту",
    status_code=HTTPStatus.CREATED,
)
async def attach_media_to_post(
    post_id: Annotated[int, Path(description="ID поста")],
    data: MediaCreate,
    media_service: MediaServiceDep,
    post_service: PostServiceDep,
) -> Media:
    """
    Привязать медиа (по URL) к существующему посту.
    """
    post: Posts | None = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")

    media = await media_service.attach_to_post(post_id=post_id, url=data.url)
    return Media.model_validate(media)


@router.get(
    "/posts/{post_id}/media",
    summary="Список медиа для поста",
)
async def list_media_for_post(
    post_id: Annotated[int, Path(description="ID поста")],
    media_service: MediaServiceDep,
    post_service: PostServiceDep,
) -> MediaList:
    """
    Получить все медиа, связанные с постом.
    """
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")

    media_list = await media_service.list_for_post(post_id)
    return MediaList.model_validate(media_list)


@router.delete(
    "/media/{media_id}",
    summary="Удалить медиа",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_media(
    media_id: Annotated[int, Path(description="ID медиа")],
    media_service: MediaServiceDep,
) -> None:
    """
    Удалить конкретное медиа.
    """
    await media_service.delete_media(media_id)
