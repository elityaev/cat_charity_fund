from typing import Optional, List, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, CharityProject, Donation
from app.constants import INV_DICT


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        """Получение объекта по id."""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> Union[List[CharityProject], List[Donation]]:
        """Получение списка объектов."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> Union[CharityProject, Donation]:
        """Создание объекта."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        """Обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @staticmethod
    async def get_not_closed_objs(
            obj: Union[CharityProject, Donation],
            session: AsyncSession
    ) -> List[Union[CharityProject, Donation]]:
        """Получает объект проект/пожертвование с неполным инвестированием."""
        not_closed_objs = await session.execute(
            select(INV_DICT[obj.__class__]).where(
                INV_DICT[obj.__class__].fully_invested == 0
            )
        )
        return not_closed_objs.scalars().all()
