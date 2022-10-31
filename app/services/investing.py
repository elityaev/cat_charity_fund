from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


async def investing(
        created_obj: Union[CharityProject, Donation],
        session: AsyncSession
) -> None:
    """Инвестирование имеющихся пожертвований в незавершенные проекты."""
    not_closed_objs = await CRUDBase.get_not_closed_objs(created_obj, session)
    if not_closed_objs:
        for not_closed_obj in not_closed_objs:
            diff_exists = not_closed_obj.full_amount - not_closed_obj.invested_amount
            diff_created = created_obj.full_amount - created_obj.invested_amount
            if diff_created > diff_exists:
                created_obj.invested_amount += diff_exists
                not_closed_obj.invested_amount += diff_exists
            elif diff_created < diff_exists:
                created_obj.invested_amount += diff_created
                not_closed_obj.invested_amount += diff_created
            elif diff_created == diff_exists:
                not_closed_obj.invested_amount += diff_exists
                created_obj.invested_amount = diff_exists
            if created_obj.invested_amount == created_obj.full_amount:
                created_obj.fully_invested = True
                created_obj.close_date = datetime.now()
            if not_closed_obj.invested_amount == not_closed_obj.full_amount:
                not_closed_obj.fully_invested = True
                not_closed_obj.close_date = datetime.now()
            session.add(created_obj)
            session.add(not_closed_obj)
            if created_obj.fully_invested:
                break
    await session.commit()
    await session.refresh(created_obj)
