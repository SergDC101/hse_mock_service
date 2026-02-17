import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend, current_user, fastapi_users
from src.endpoints.router import router as endpoint_router
from src.groups.router import router as groups_router
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate

app = FastAPI()


app.include_router(endpoint_router)
app.include_router(groups_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


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
