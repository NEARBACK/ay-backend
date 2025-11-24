# tests/test_donation.py
from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_donation_flow_create_and_confirm(client: AsyncClient) -> None:
    """
    Полный happy-path:
    - создаём пост от автора (он же донор, чтобы не заморачиваться);
    - создаём донат на этот пост;
    - подтверждаем донат (tx_hash);
    """
    wallet = "EQB_TEST_WALLET_DONOR"

    headers = {"X-Wallet-Address": wallet}

    # 1) создаём пост
    post_resp = await client.post(
        "/api/post/posts",
        headers=headers,
        json={
            "text": "Support me with TON 🚀",
            "recommended_amount_nanoton": 50_000_000,
        },
    )
    assert post_resp.status_code == HTTPStatus.CREATED
    post_data: dict[str, Any] = post_resp.json()
    post_id = post_data["id"]

    # 2) создаём донат
    donation_resp = await client.post(
        f"/api/donation/posts/{post_id}/donations",
        headers=headers,
        json={
            # можно не передавать, если в DonationCreate amount_nanoton optional
            "amount_nanoton": 50_000_000,
        },
    )
    assert donation_resp.status_code == HTTPStatus.CREATED
    body = donation_resp.json()
    assert "donation" in body
    assert "ton_transaction" in body

    donation = body["donation"]
    ton_tx = body["ton_transaction"]

    assert donation["post_id"] == post_id
    assert donation["status"] == "PENDING"
    assert ton_tx["to"]  # кошелёк автора
    assert ton_tx["amount_nanoton"] == 50_000_000

    donation_id = donation["id"]

    # 3) подтверждаем донат (как будто Tonkeeper вернул tx_hash)
    confirm_resp = await client.post(
        f"/api/donation/donations/{donation_id}/confirm",
        json={
            "tx_hash": "SOME_FAKE_TX_HASH_FOR_TEST",
        },
    )
    assert confirm_resp.status_code == HTTPStatus.OK
    confirmed = confirm_resp.json()
    assert confirmed["id"] == donation_id
    assert confirmed["status"] == "CONFIRMED"
    assert confirmed["tx_hash"] == "SOME_FAKE_TX_HASH_FOR_TEST"
