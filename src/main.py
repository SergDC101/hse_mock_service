import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend, current_user, fastapi_users
from src.config import MONGO_LINK, MONGO_BASE
from src.database import get_async_session
from src.endpoints.models import endpoint
from src.endpoints.router import router as endpoint_router
from src.groups.models import group
from src.groups.router import router as groups_router
from src.auth.models import User, user
from src.auth.schemas import UserRead, UserCreate
from src.mongo import MongoManager

app = FastAPI()


app.include_router(endpoint_router)
app.include_router(groups_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

@app.get("/auth/user_data", tags=["auth"])
def get_user_data(user: User = Depends(current_user)):
    return user.username

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

@app.get("/api/{full_path:path}")
async def get_data(full_path: str,
                   session: AsyncSession = Depends(get_async_session)):
    path_list=  full_path.split("/")
    print(path_list)
    # Проверяем что путь содержит минимум 3 части
    if len(path_list) < 3:
        raise HTTPException(
            status_code=400,
            detail="Invalid path format. Expected: username/group/endpoint"
        )
    username = path_list[0]
    group_name = path_list[1]
    route_name = path_list[2]

    # Простой запрос для получения endpoint_id
    query = select(endpoint.c.id).where(
        and_(
            user.c.username == username,
            group.c.endpoint == group_name,
            endpoint.c.path == route_name,
            user.c.id == group.c.user_id,
            group.c.id == endpoint.c.group_id
        )
    )

    result = await session.execute(query)
    endpoint_id = result.scalar()

    if not endpoint_id:
        raise HTTPException(
            status_code=404,
            detail="Endpoint not found"
        )

    with MongoManager(MONGO_LINK, MONGO_BASE) as mongo:
        data = mongo.find_one(username, endpoint_id)['data']

    return data






origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return user


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonyam"

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8086, reload=True)
