from fastapi import APIRouter

from app.api.endpoints import charity_project, donation
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Маршруты аутентификации
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(
        UserCreate, UserRead
    ),  # type: ignore[type-var]
    prefix='/auth',
    tags=['auth'],
)

# Маршруты управления профилями
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)

# Доменные маршруты проекта
router.include_router(
    charity_project.router,
    prefix='/charity_project',
    tags=['charity_project'],
)
router.include_router(
    donation.router,
    prefix='/donation',
    tags=['donation'],
)