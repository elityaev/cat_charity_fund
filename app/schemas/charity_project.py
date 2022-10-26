from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    """Схема создания объекта."""
    pass


class CharityProjectUpdate(CharityProjectBase):
    """Схема обновления проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """Схема проекта, полученного из БД."""
    id: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
