from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped, mapped_column, declared_attr
)


class CommonMixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
