from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)


class CharityProjectCreate(CharityProjectBase):
    """Схема создания проекта."""
    model_config = ConfigDict(extra='forbid')

    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(BaseModel):
    """Схема обновления проекта."""
    model_config = ConfigDict(extra='forbid')

    name: str | None = Field(None, min_length=5, max_length=100)
    description: str | None = Field(None, min_length=10)
    full_amount: int | None = Field(None, gt=0)


class CharityProjectDB(CharityProjectBase):
    """Схема ответа API."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_amount: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime | None = None
