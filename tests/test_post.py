# tests/test_post.py
from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_and_list_posts(client: AsyncClient) -> None:
    wallet = "EQB_TEST_WALLET_POST"

    headers = {"X-Wallet-Address": wallet}

    # 1) создаём пост
    create_resp = await client.post(
        "/api/post/posts",
        headers=headers,
        json={
            "text": "Hello TON World!",
            "recommended_amount_nanoton": 100_000_000,
        },
    )
    assert create_resp.status_code == HTTPStatus.CREATED
    created: dict[str, Any] = create_resp.json()
    assert created["text"] == "Hello TON World!"
    assert created["recommended_amount_nanoton"] == 100_000_000
    assert "id" in created
    post_id = created["id"]

    # 2) получаем его через GET /posts/{id}
    get_resp = await client.get(f"/api/post/posts/{post_id}")
    assert get_resp.status_code == HTTPStatus.OK
    got = get_resp.json()
    assert got["id"] == post_id
    assert got["text"] == "Hello TON World!"

    # 3) проверяем, что он есть в ленте
    list_resp = await client.get("/api/post/posts", params={"limit": 10, "page": 0})
    assert list_resp.status_code == HTTPStatus.OK
    items = list_resp.json()
    # RootModel[list[Post]] → сам JSON это просто список
    assert isinstance(items, list)
    assert any(p["id"] == post_id for p in items)
