from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class DonationCreate(BaseModel):
    """Схема создания пожертвования"""
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreateDB(DonationCreate):
    """Схема пожертвования из БД после создания"""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationListDB(DonationCreateDB):
    """Схема всех пожертвований из БД"""
    user_id: int
    invested_amount: int
    fully_invested: bool


class DonationUserDB(DonationCreateDB):
    """Схема пожертвований пользователя из БД"""
    pass
