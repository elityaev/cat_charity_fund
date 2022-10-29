from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> CharityProject:
        """Получение проекта по имени."""
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return project.scalars().first()


project_crud = CRUDCharityProject(CharityProject)
