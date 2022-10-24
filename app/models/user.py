from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer

from app.core.db import UserBase


class User(SQLAlchemyBaseUserTable[int], UserBase):
    pass
