from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base


class Donation(Base):
    comment = Column(Text)

    def __repr__(self):
        return str(self.id)