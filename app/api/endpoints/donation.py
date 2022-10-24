from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import investing
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationCreateDB, DonationListDB

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreateDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session)
    await investing(session)
    return new_donation

@router.get(
    '/',
    response_model=list[DonationListDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    all_donation = await donation_crud.get_multi(session)
    return all_donation
