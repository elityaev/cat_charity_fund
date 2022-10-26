from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    pass

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User,
    ):
        """Получение всех пожертвований пользователя."""
        donations = await session.execute(
            select(Donation). where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)