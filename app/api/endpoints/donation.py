from typing import Annotated, cast

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import invest_in_projects

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: SessionDep,
    user: User = Depends(current_user),
) -> DonationDB:
    """
    Создать новое пожертвование и запустить авто-инвестирование.
    """
    donation = await donation_crud.create(
        session, donation_in, user_id=user.id
    )

    await invest_in_projects(session)
    await session.commit()
    await session.refresh(donation)

    return cast(DonationDB, donation)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: SessionDep,
    user: User = Depends(current_user),
) -> list[DonationDB]:
    """
    Получить список пожертвований текущего пользователя.
    """
    result = await session.execute(
        select(Donation).where(Donation.user_id == user.id)
    )
    donations = result.scalars().all()
    return cast(list[DonationDB], list(donations))


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep,
) -> list[DonationFullInfoDB]:
    """
    Получить список всех пожертвований (только для суперпользователей).
    """
    donations = await donation_crud.get_multi(session)
    return cast(list[DonationFullInfoDB], donations)