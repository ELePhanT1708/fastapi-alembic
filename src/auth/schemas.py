import uuid
from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    email: EmailStr
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    username: str = Field(max_length=30)
    role_id: int
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

