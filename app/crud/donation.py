from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class DonationCRUD(CRUDBase):
    """
    CRUD-класс для выполнения операций доступа к данным о пожертвованиях.
    """

    async def get_uninvested_donations(
        self, session: AsyncSession
    ) -> list[Donation]:
        """
        Получить список пожертвований, у которых invested_amount < full_amount.
        Результат сортируется по дате создания
        (принцип FIFO для автоматического инвестирования).
        """
        result = await session.execute(
            select(Donation)
            .where(Donation.full_amount > Donation.invested_amount)
            .order_by(Donation.create_date)
        )
        return list(result.scalars().all())

    async def get_donation_ids_by_user(
        self, user_id: int, session: AsyncSession
    ) -> list[int]:
        """
        Получить список ID всех пожертвований конкретного пользователя.
        Запрашивает только колонку id для оптимизации производительности.
        """
        result = await session.execute(
            select(Donation.id)
            .where(Donation.user_id == user_id)  # type: ignore[attr-defined]
        )
        return list(result.scalars().all())


donation_crud = DonationCRUD(Donation)