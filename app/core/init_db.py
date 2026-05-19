from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.user import UserManager
from app.models.user import User
from fastapi_users.db import SQLAlchemyUserDatabase


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

        user_create = user_manager.parse_user_create({
            "email": email.lower(),
            "password": password,
            "is_active": True,
            "is_verified": False,
            "is_superuser": is_superuser,
        })

        created_user: User = await user_manager.create(
            user_create, safe=False, request=None
        )
        await session.commit()
        await session.refresh(created_user)

        return created_user
