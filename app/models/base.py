from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import (
    Mapped, mapped_column, declared_attr
)

from app.core.db import Base


class CommonMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )


class InvestmentTarget(CommonMixin, Base):
    """Абстрактный базовый класс для проектов и пожертвований."""
    __abstract__ = True

    full_amount: Mapped[int] = mapped_column(Integer)
    invested_amount: Mapped[int] = mapped_column(Integer, default=0)
    fully_invested: Mapped[bool] = mapped_column(Boolean, default=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    close_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
