from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest_in_projects(
    session: AsyncSession,
) -> list[CharityProject | Donation]:
    """
    Автоматически распределить непогашенные пожертвования по открытым проектам.
    Использует алгоритм двух указателей: сложность O(N + M).
    Возвращает список изменённых ORM-объектов.
    Коммит выполняется вызывающим кодом.
    """
    donations = await donation_crud.get_uninvested_donations(session)
    projects = cast(
        list[CharityProject], await charity_project_crud.get_multi(session)
    )

    # Оставляем только открытые проекты и сортируем по дате создания (FIFO)
    open_projects = [p for p in projects if not p.fully_invested]
    open_projects.sort(key=lambda p: p.create_date)

    updated_objects: list[CharityProject | Donation] = []
    donation_idx = 0
    project_idx = 0

    while donation_idx < len(donations) and project_idx < len(open_projects):
        donation = donations[donation_idx]
        project = open_projects[project_idx]

        donation_remaining = donation.full_amount - donation.invested_amount
        project_remaining = project.full_amount - project.invested_amount

        invest_amount = min(donation_remaining, project_remaining)

        donation.invested_amount += invest_amount
        project.invested_amount += invest_amount

        updated_objects.append(donation)
        updated_objects.append(project)

        if donation.invested_amount == donation.full_amount:
            donation_idx += 1

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project_idx += 1

    return updated_objects