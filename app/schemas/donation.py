from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class DonationCreate(BaseModel):
    """Схема создания пожертвования."""
    model_config = ConfigDict(extra='forbid')

    full_amount: int = Field(..., gt=0)
    comment: str | None = None


class DonationDB(BaseModel):
    """Схема ответа для пользователя."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_amount: int
    comment: str | None = None
    create_date: datetime


class DonationFullInfoDB(DonationDB):
    """Схема ответа для суперпользователя."""
    user_id: int
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime | None = None
