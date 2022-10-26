from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationCreate, DonationCreateDB,
    DonationListDB, DonationUserDB
)
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreateDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Внесение пожертвований - для аутентифицированного пользователя."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing(session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationListDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Просмотр всех пожертвований - только для суперюзеров."""
    all_donation = await donation_crud.get_multi(session)
    return all_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получает список пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(session, user)
    return donations
