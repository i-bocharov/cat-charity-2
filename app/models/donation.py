from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import InvestmentTarget


class Donation(InvestmentTarget):
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
