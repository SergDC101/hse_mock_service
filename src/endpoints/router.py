import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.config import MONGO_LINK, MONGO_BASE
from src.database import get_async_session
from src.endpoints.models import endpoint
from src.endpoints.schemas import EndpointCreate
from src.groups.models import group
from src.mongo import MongoManager

router = APIRouter(
    prefix="/endpoint",
    tags=["Endpoint"]
)


@router.post("/")
async def create_endpoint(
        new_endpoint: EndpointCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    data = new_endpoint.dict()

    group_query = select(group).where(
        group.c.endpoint == data['group_name'],
        group.c.user_id == user.id
    )
    group_result = await session.execute(group_query)
    existing_group = group_result.first()

    if not existing_group:
        # Если группа не найдена, можно создать новую или вернуть ошибку
        return HTTPException(status_code=404,
                             detail=f"Группа '{data['group_name']}' не найдена или у пользователя нет прав")

    group_id = existing_group.id

    # Подготавливаем данные для вставки
    endpoint_data = {
        "path": data['path'],
        "method": data['method'].upper(),  # Приводим метод к верхнему регистру
        "group_id": group_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    insert_query = insert(endpoint).values(**endpoint_data)
    result = await session.execute(insert_query)
    await session.commit()

    json_data = json.loads(data['json_data'])

    with MongoManager(MONGO_LINK, MONGO_BASE) as mongo:
        mongo.insert_one(user.username, {
            "group": data['group_name'],
            "endpoint_id": result.inserted_primary_key[0],
            "router": data['path'],
            "method": data['method'].upper(),
            "data": json_data,

        })

    # Возвращаем ID созданной записи
    return {"success": True, "data": []}


@router.get("/id/")
async def get_endpoint(id: int,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(endpoint).where(endpoint.c.id == id)
    result = await session.execute(query)
    result = dict(result.mappings().first())

    with MongoManager(MONGO_LINK, MONGO_BASE) as mongo:
        mongo_data = mongo.find_one(user.username, id)

    print(mongo_data)
    result['json'] = mongo_data['data']

    return result


@router.put("/")
async def update_endpoint(
        new_endpoint: EndpointCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.delete("/")
async def delete_endpoint(
        group_name: str,
        path: str,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass
