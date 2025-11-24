from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.param_functions import Depends

from db.models.post import Posts
from db.models.user import Users
from schemas.post import Post, PostCreate, PostList
from services.post_service.service import PostService
from src.api.dependencies import get_current_user, get_post_service

router = APIRouter()


@router.post(
    "/posts",
    summary="Создать пост",
    status_code=HTTPStatus.CREATED,
)
async def create_post(
    data: PostCreate,
    current_user: Users = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
) -> Post:
    post: Posts = await post_service.create_post(author_id=current_user.id, data=data)
    return Post.model_validate(post)


@router.get(
    "/posts",
    summary="Получить ленту постов",
)
async def list_posts(
    limit: Annotated[int, Query(description="Размер страницы")] = 10,
    page: Annotated[int, Query(description="Индекс страницы (offset)")] = 0,
    post_service: PostService = Depends(get_post_service),
) -> PostList:
    """
    Лента постов. `page` используется как offset (как в dummy).
    """
    posts = await post_service.list_posts(limit=limit, offset=page)
    return PostList.model_validate(posts)


@router.get(
    "/posts/{post_id}",
    summary="Получить один пост",
)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
) -> Post:
    post = await post_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")
    return Post.model_validate(post)
