from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_project_exists, investing
from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB,
    CharityProjectUpdate, get_project_by_id
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    await investing(session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charity_projects = await project_crud.get_multi(
        session
    )
    return all_charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    project = await get_project_by_id(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    project = await project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    project = await project_crud.remove(project, session)
    return project
