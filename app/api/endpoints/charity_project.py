from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_project_exists,
    check_amount_invested, check_fully_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создание проектов - только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    await investing(new_project, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Получение списка всех проектов"""
    all_charity_projects = await project_crud.get_multi(
        session
    )
    return all_charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """ТИзменение проекта - только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    check_fully_invested(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_amount_invested(project, obj_in.full_amount)
    project = await project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Удаление проекта - только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    project = check_amount_invested(project)
    project = await project_crud.remove(project, session)
    return project
