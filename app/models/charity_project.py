from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import InvestmentTarget


class CharityProject(InvestmentTarget):
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
