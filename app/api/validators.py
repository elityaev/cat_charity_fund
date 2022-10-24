from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.schemas.charity_project import get_project_by_name, get_project_by_id


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    project_id = await get_project_by_name(project_name, session)
    if project_id:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует'
        )

async  def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await get_project_by_id(project_id,session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return project

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
        if (
                projects_list[0].invested_amount
                + donations_list[0].full_amount
                - donations_list[0].invested_amount
                <= projects_list[0].full_amount
        ):
            projects_list[0].invested_amount += (
                    donations_list[0].full_amount
                    - donations_list[0].invested_amount
            )
            donations_list[0].invested_amount = donations_list[0].full_amount
            donations_list[0].fully_invested = True
            donations_list[0].close_date = datetime.now()
            session.add(donations_list[0])
            session.add(projects_list[0])
            await session.commit()
            await session.refresh(donations_list[0])
            await session.refresh(projects_list[0])
            donations_list.remove(donations_list[0])
        else:
            shortage = (
                    projects_list[0].full_amount
                    - projects_list[0].invested_amount)
            donations_list[0].invested_amount = shortage
            projects_list[0].invested_amount = projects_list[0].full_amount
            projects_list[0].fully_invested = True
            projects_list[0].close_date = datetime.now()
            session.add(projects_list[0])
            session.add(donations_list[0])
            await session.commit()
            await session.refresh(projects_list[0])
            await session.refresh(donations_list[0])
            projects_list.remove(projects_list[0])






