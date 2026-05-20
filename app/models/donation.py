from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import InvestmentTarget


class Donation(InvestmentTarget):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    comment: Mapped[str | None] = mapped_column(String, nullable=True)
