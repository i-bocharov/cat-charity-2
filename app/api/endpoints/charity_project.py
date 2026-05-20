from typing import Annotated, cast

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_ge_invested,
    check_project_exists,
    check_project_name_duplicate,
    check_project_no_investments,
    check_project_not_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import CharityProject
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_all_projects(
    session: SessionDep,
) -> list[CharityProjectDB]:
    """
    Получить список всех благотворительных проектов.
    """
    projects = await charity_project_crud.get_multi(session)
    return cast(list[CharityProjectDB], projects)


@router.get(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_project(
    project_id: int,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Получить конкретный проект по его ID.
    """
    project = await check_project_exists(project_id, session)
    return cast(CharityProjectDB, project)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    project_in: CharityProjectCreate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Создать новый благотворительный проект (только для суперпользователей).
    """
    await check_project_name_duplicate(project_in.name, session)
    project = await charity_project_crud.create(session, project_in)
    return cast(CharityProjectDB, project)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Обновить поля проекта (только для суперпользователей).
    """
    project = await check_project_exists(project_id, session)
    await check_project_not_closed(project)

    if project_in.full_amount is not None:
        await check_full_amount_ge_invested(
            project_in.full_amount, project.invested_amount
        )
    if project_in.name is not None and project_in.name != project.name:
        await check_project_name_duplicate(project_in.name, session)

    updated = await charity_project_crud.update(session, project, project_in)
    updated_project = cast(CharityProject, updated)

    # Автоматическое закрытие проекта, если собранная сумма >= целевой
    if (
        updated_project.invested_amount >= updated_project.full_amount
        and not updated_project.fully_invested
    ):
        updated_project.fully_invested = True
        updated_project.close_date = datetime.now(timezone.utc)
        await session.commit()
        await session.refresh(updated_project)

    return cast(CharityProjectDB, updated_project)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: SessionDep,
) -> CharityProjectDB:
    """
    Удалить проект (только для суперпользователей).
    """
    project = await check_project_exists(project_id, session)
    await check_project_not_closed(project)
    await check_project_no_investments(project)
    deleted = await charity_project_crud.remove(session, project)
    return cast(CharityProjectDB, deleted)