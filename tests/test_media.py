# tests/test_media.py
from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_media_flow_attach_list_and_delete(client: AsyncClient) -> None:
    """
    Happy-path по работе с медиа:
    - создаём пост;
    - привязываем к нему медиа (по URL);
    - получаем список медиа и проверяем, что оно там есть;
    - удаляем медиа;
    - убеждаемся, что список медиа пуст.
    """
    wallet = "EQB_TEST_WALLET_MEDIA"
    headers = {"X-Wallet-Address": wallet}

    # 1) создаём пост
    post_resp = await client.post(
        "/api/post/posts",
        headers=headers,
        json={
            "text": "Post with media 🎨",
            "recommended_amount_nanoton": 100_000_000,
        },
    )
    assert post_resp.status_code == HTTPStatus.CREATED
    post_data: dict[str, Any] = post_resp.json()
    post_id = post_data["id"]

    # 2) привязываем медиа к посту
    media_url = "https://example.com/image1.jpg"
    attach_resp = await client.post(
        f"/api/media/posts/{post_id}/media",
        json={"url": media_url},
    )
    assert attach_resp.status_code == HTTPStatus.CREATED
    media_data: dict[str, Any] = attach_resp.json()
    assert media_data["post_id"] == post_id
    assert media_data["url"] == media_url
    media_id = media_data["id"]

    # 3) смотрим список медиа у поста
    list_resp = await client.get(f"/api/media/posts/{post_id}/media")
    assert list_resp.status_code == HTTPStatus.OK
    media_list: list[dict[str, Any]] = list_resp.json()
    assert len(media_list) == 1
    assert media_list[0]["id"] == media_id
    assert media_list[0]["url"] == media_url

    # 4) удаляем медиа
    delete_resp = await client.delete(f"/api/media/media/{media_id}")
    assert delete_resp.status_code == HTTPStatus.NO_CONTENT

    # 5) список медиа теперь пуст
    list_after_delete_resp = await client.get(f"/api/media/posts/{post_id}/media")
    assert list_after_delete_resp.status_code == HTTPStatus.OK
    media_list_after: list[dict[str, Any]] = list_after_delete_resp.json()
    assert media_list_after == []


@pytest.mark.anyio
async def test_attach_media_nonexistent_post_returns_404(client: AsyncClient) -> None:
    """
    Попытка привязать медиа к несуществующему посту должна вернуть 404.
    """
    fake_post_id = 999999

    resp = await client.post(
        f"/api/media/posts/{fake_post_id}/media",
        json={"url": "https://example.com/nonexistent.jpg"},
    )

    assert resp.status_code == HTTPStatus.NOT_FOUND
    body = resp.json()
    # в роутере мы поднимали detail="Post not found"
    assert body.get("detail") == "Post not found"
