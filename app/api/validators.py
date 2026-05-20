from typing import cast

from fastapi import HTTPException
from fastapi_users.exceptions import InvalidPasswordException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """
    Проверить уникальность имени благотворительного проекта.
    Вызывает HTTP 400, если проект с таким именем уже существует в БД.
    """
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверить существование проекта по ID.
    Возвращает объект CharityProject или вызывает HTTP 404.
    Позволяет избежать повторного запроса к БД в эндпоинтах.
    """
    project = await charity_project_crud.get(
        session=session, obj_id=project_id
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    # Явное приведение типа удовлетворяет строгий анализатор
    # без использования подавления предупреждений.
    return cast(CharityProject, project)


async def check_project_not_closed(project: CharityProject) -> None:
    """
    Запретить обновление или удаление полностью инвестированного проекта.
    Вызывает HTTP 400, если флаг fully_invested установлен в True.
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя обновить или удалить полностью инвестированный проект!'
            ),
        )


async def check_project_no_investments(project: CharityProject) -> None:
    """
    Запретить удаление проекта, в который уже внесены средства.
    Вызывает HTTP 400, если invested_amount > 0.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=(
                'В проект уже внесены средства, удаление невозможно!'
            ),
        )


async def check_full_amount_ge_invested(
    new_amount: int, current_invested: int
) -> None:
    """
    Проверить, что новая целевая сумма не меньше уже инвестированной.
    Вызывает HTTP 422 при нарушении бизнес-правила.
    """
    if new_amount < current_invested:
        raise HTTPException(
            status_code=422,
            detail=(
                'Значение full_amount не может быть '
                'меньше уже вложенной суммы!'
            ),
        )


MIN_PASSWORD_LENGTH = 3


def validate_password_strength(password: str) -> None:
    """
    Проверяет сложность пароля.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise InvalidPasswordException(
            reason=(
                f"Password should be at least {MIN_PASSWORD_LENGTH} characters"
            )
        )