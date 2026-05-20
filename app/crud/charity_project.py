from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    """
    CRUD-класс для выполнения операций доступа к
    данным благотворительных проектов.
    """

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> int | None:
        """
        Получить ID проекта по его уникальному имени.
        Запрашивает только колонку id для оптимизации
        потребления памяти и времени БД.
        Возвращает None, если проект с таким именем не найден.
        """
        result = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return result.scalars().first()


charity_project_crud = CharityProjectCRUD(CharityProject)