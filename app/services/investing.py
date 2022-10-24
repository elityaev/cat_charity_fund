from select import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def investing(session: AsyncSession):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False
        )
    )
    projects_list = projects.scalars().all()
    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested == False
        )
    )
    donations_list = donations.scalars().all()
    while projects_list and donations_list:
        if donations_list[0].full_amount <= projects_list[0].full_amount:
            projects_list[0].full_amount -= donations_list[0].full_amount
            donations_list[0].full_amount = 0
            donations_list.pop()
        else:
            donations_list[0].full_amount -= projects_list[0].full_amount
            projects_list[0].full_amount = 0
            projects_list.pop()
