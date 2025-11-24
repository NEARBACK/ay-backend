from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from db.models.donations import Donations
from db.models.user import Users
from schemas.donation import DonationConfirm, DonationCreate, DonationSchema
from services.donation_service.service import DonationService
from src.api.dependencies import get_current_user, get_donation_service

router = APIRouter()


@router.post(
    "/posts/{post_id}/donations",
    summary="Создать донат (инициировать перевод через TonConnect)",
    status_code=HTTPStatus.CREATED,
)
async def create_donation(
    post_id: int,
    body: DonationCreate,
    current_user: Users = Depends(get_current_user),
    donation_service: DonationService = Depends(get_donation_service),
) -> dict[str, Any]:
    """
    Создаём запись доната и возвращаем параметры для TonConnect:
    - to (кошелёк автора)
    - amount_nanoton
    - comment
    """
    donation: Donations = await donation_service.create_donation(
        post_id=post_id,
        from_wallet=current_user.wallet_address,
        data=body,
    )

    dto = DonationSchema.model_validate(donation)

    ton_tx = {
        "to": donation.to_wallet,
        "amount_nanoton": donation.amount_nanoton,
        "comment": donation.comment,
    }

    return {
        "donation": dto,
        "ton_transaction": ton_tx,
    }


@router.post(
    "/donations/{donation_id}/confirm",
    summary="Подтвердить донат после Tonkeeper (tx_hash)",
)
async def confirm_donation(
    donation_id: int,
    body: DonationConfirm,
    donation_service: DonationService = Depends(get_donation_service),
) -> DonationSchema:
    donation = await donation_service.confirm_donation(donation_id, body)
    if not donation:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Donation not found")
    return DonationSchema.model_validate(donation)
