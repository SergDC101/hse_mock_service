from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.groups.models import group
from src.groups.schemas import GroupCreate

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)


@router.post("/")
async def set_group(
        new_group: GroupCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/")
async def get_group(
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    query = select(group.c.id, group.c.name, group.c.endpoint,
                   group.c.active, group.c.description, group.c.created_at,
                   group.c.updated_at,
                   ).where(group.c.user_id == user.id)
    result = await session.execute(query)
    return result.mappings().all()


@router.put("/")
async def update_group(
        new_group: GroupCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/")
async def delete_group(
        group_name: str,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass
