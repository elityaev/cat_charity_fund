from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    """Модель для пожертвований"""
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
