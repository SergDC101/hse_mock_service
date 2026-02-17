from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.auth.models import User
from src.database import get_async_session
from src.endpoints.models import endpoint
from src.endpoints.schemas import EndpointCreate

router = APIRouter(
    prefix="/endpoint",
    tags=["Endpoint"]
)


@router.post("/")
async def set_endpoint(
        new_endpoint: EndpointCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    pass


@router.get("/{id}")
async def get_endpoint(id: int,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(endpoint).where(endpoint.c.id == id)
    result = await session.execute(query)
    result = dict(result.mappings().first())
    result['json'] = '{"test": "test"}'

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
