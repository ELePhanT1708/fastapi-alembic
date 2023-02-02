import time

import aioredis
from fastapi_redis_cache import FastApiRedisCache, cache


from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

from src.auth.models import User
from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.auth import current_user

from src.operations.router import router as router_operations

from src.celery_tasks.router import router as router_celery

app = FastAPI(
    title="Trading App"
)

app.include_router(router_operations)
app.include_router(router_celery)

#  Auth endpoints
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

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/long-route")
@cache(expire=30)
def long_operations_with_cache(something: str):
    time.sleep(3)
    return f"Hello, {something}"


@app.get("/unprotected-route")
def protected_route():
    return f"Hello, I don't know who are u! "


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url='redis://127.0.0.1:6379',
    )


# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


