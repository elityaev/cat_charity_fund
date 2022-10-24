from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)



class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    @validator('full_amount')
    def name_cannot_be_null(cls, full_amount, values):
        if 'full_amount' in values and full_amount <= values['invested_amount']:
            raise ValueError('Новая сумма не должна быть меньше уже собранной!')
        return full_amount

class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


async def get_project_by_id(
        project_id: int,
        session: AsyncSession,
):
    project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    return project.scalars().first()


async def get_project_by_name(
        project_name: str,
        session: AsyncSession,
):
    project = await session.execute(
        select(CharityProject).where(
            CharityProject.name == project_name
        )
    )
    return project.scalars().first()
