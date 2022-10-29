from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase


async def investing(created_obj, session: AsyncSession):
    """Инвестирование имеющихся пожертвований в незавершенные проекты."""
    not_closed_obj = await CRUDBase.get_not_closed_obj(created_obj, session)
    if not_closed_obj:
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
        await session.commit()
        await session.refresh(created_obj)
        await session.refresh(not_closed_obj)
        if created_obj.fully_invested:
            return await investing(not_closed_obj, session)
        if not_closed_obj.fully_invested:
            return await investing(created_obj, session)
