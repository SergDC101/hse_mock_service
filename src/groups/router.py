from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.endpoints.models import endpoint
from src.groups.models import group
from src.groups.schemas import GroupCreate

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)


@router.post("/")
async def create_group(
        new_group: GroupCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    data = new_group.dict()
    print(data)
    data['user_id'] = user.id
    stmt = insert(group).values(data)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
    # проверить что у пользователя нет группы с таким же endpoint
    # если есть отдаем ошибку
    # в ином случае создаем запись в бд


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


@router.get("/{id}")
async def get_group_by_id(
                    group_id: int,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):

    query = select(group).filter(
        group.c.id == group_id,
        group.c.user_id == user.id
    )
    group_data = await session.execute(query)
    group_data = group_data.first()

    if not group_data:
        return None

    query = select(endpoint).where(endpoint.c.group_id == group_id)
    result = await session.execute(query)

    data = result.mappings().all()

    return {
                "id": group_data.id,
                "name": group_data.name,
                "description": group_data.description,
                "active": group_data.active,
                "endpoint": group_data.endpoint,
                "data": data
            }


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
