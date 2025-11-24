# tests/test_user.py
from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_auth_ton_connect_and_me(client: AsyncClient) -> None:
    wallet = "EQB_TEST_WALLET_USER"

    # 1) auth/ton-connect — создаёт или возвращает пользователя
    resp = await client.post(
        "/api/user/auth/ton-connect",
        json={
            "wallet_address": wallet,
            "display_name": "Test User",
        },
    )
    assert resp.status_code == HTTPStatus.OK
    data = resp.json()
    assert data["wallet_address"] == wallet
    assert data["display_name"] == "Test User"

    # 2) /me — по X-Wallet-Address должен вернуть того же пользователя
    resp_me = await client.get(
        "/api/user/me",
        headers={"X-Wallet-Address": wallet},
    )
    assert resp_me.status_code == HTTPStatus.OK
    me = resp_me.json()
    assert me["wallet_address"] == wallet
    # display_name может быть None, если создавался через get_current_user,
    # но здесь он уже есть, так что проверим:
    assert me["display_name"] == "Test User"
