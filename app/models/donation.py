from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    comment = Column(Text)

    def __repr__(self):
        return str(self.id)