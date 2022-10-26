from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    """Инвестирование имеющихся пожертвований в незавершенные проекты."""
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == 0
        )
    )
    projects = projects.scalars().first()
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == 0
        )
    )
    donations = donations.scalars().first()
    if projects and donations:
        shortage_donation = projects.full_amount - projects.invested_amount
        remaining_donations = donations.full_amount - donations.invested_amount
        if shortage_donation > remaining_donations:
            projects.invested_amount += remaining_donations
            donations.invested_amount += remaining_donations
            donations.fully_invested = True
            donations.close_date = datetime.now()
        elif shortage_donation == remaining_donations:
            donations.invested_amount = remaining_donations
            donations.fully_invested = True
            donations.close_date = datetime.now()
            projects.invested_amount = remaining_donations
            projects.fully_invested = True
            projects.close_date = datetime.now()
        else:
            donations.invested_amount = shortage_donation
            projects.invested_amount = shortage_donation
            projects.fully_invested = True
            projects.close_date = datetime.now()
        session.add(donations)
        session.add(projects)
        await session.commit()
        await session.refresh(donations)
        await session.refresh(projects)
        return await investing(session)
