from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    pass


project_crud = CRUDCharityProject(CharityProject)


async def investing(session: AsyncSession):
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested == False
        )
    )
    project_list = projects.scalars().all()
    print(project_list)