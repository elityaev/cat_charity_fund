from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.models import Donation
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """Проверка уникальности имени проекта."""
    project = await project_crud.get_project_by_name(
        project_name, session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта."""
    project = await project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


def check_amount_invested(
        obj: Union[CharityProject, Donation],
        new_amount: int = None
) -> Union[CharityProject, Donation]:
    """Проверка условий редактирования и удаления проекта."""
    invested = obj.invested_amount
    if new_amount:
        if invested > new_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Новая требуемая сумма не может быть меньше уже внесенной'
            )
    elif invested > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return obj


def check_fully_invested(
        obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """Проверка - закрыт ли проект."""
    if obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return obj
