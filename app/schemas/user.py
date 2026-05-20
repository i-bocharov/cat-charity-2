from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Схема чтения пользователя (ответ GET/POST).
    """
    ...


class UserCreate(schemas.BaseUserCreate):
    """
    Схема создания пользователя (тело POST /auth/register).
    """
    ...


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема обновления пользователя (тело PATCH /users/me).
    """
    ...