from sqlalchemy import select
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.db import AsyncSessionLocal
from app.core.user import UserManager
from app.models.user import User
from app.schemas import UserCreate


async def create_user(
    email: str,
    password: str,
    is_superuser: bool = False,
) -> User:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(
                User.email == email.lower()  # type: ignore[arg-type]
            )
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return existing_user

        user_db: SQLAlchemyUserDatabase[User, int] = SQLAlchemyUserDatabase(
            session, User
        )
        user_manager = UserManager(user_db)

        user_create = UserCreate(email=email.lower(), password=password)

        created_user: User = await user_manager.create(
            user_create, safe=False, request=None
        )

        if is_superuser:
            created_user.is_superuser = True

        await session.commit()
        await session.refresh(created_user)

        return created_user
