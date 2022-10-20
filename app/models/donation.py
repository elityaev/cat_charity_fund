from sqlalchemy import Column, Text

from app.core.db import Base


class Donation(Base):
    comment = Column(Text)