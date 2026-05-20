from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


class CRUDBase:
    """
    Базовый класс для выполнения асинхронных CRUD-операций с
    SQLAlchemy моделями.
    """

    def __init__(self, model: type[Base]):
        """
        Инициализация CRUD-класса с конкретной моделью.
        """
        self.model = model

    async def get(self, session: AsyncSession, obj_id: int) -> Base | None:
        """
        Получить объект модели по его ID.
        """
        result = await session.execute(select(self.model).where(
            self.model.id == obj_id  # type: ignore[attr-defined]
        ))
        return result.scalars().first()

    async def get_multi(self, session: AsyncSession) -> list[Base]:
        """
        Получить список всех объектов модели.
        """
        result = await session.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, obj_in: BaseModel) -> Base:
        """
        Создать новый объект в базе данных из Pydantic-схемы.
        """
        obj_dict = obj_in.model_dump()
        db_obj = self.model(**obj_dict)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: Base, obj_in: BaseModel
    ) -> Base:
        """
        Обновить поля существующего объекта данными из Pydantic-схемы.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, db_obj: Base) -> Base:
        """
        Удалить объект из базы данных.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj