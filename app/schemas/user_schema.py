from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    phone_number: str = Field(
        min_length=11,
        max_length=11,
        regex=r'^7[0-9]{10,10}$',
    )


class UserBaseSchema(UserBase):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    patronymic: Optional[str] = Field(max_length=50)
    email: Optional[EmailStr]
    country: str = Field(max_length=50)


class UserCreateSchema(UserBaseSchema):
    ...


class UserUpdateSchema(UserBaseSchema):
    ...


class UserDBSchema(UserBaseSchema):
    id: int
    user_id: str

    class Config:
        orm_mode = True


class UserSchemaOnGet(UserDBSchema):
    country_code: Optional[str]


class UserSchemaOnCreate(UserDBSchema):
    date_created: datetime
    date_modified: datetime


class UserSchemaOnDelete(UserDBSchema):
    ...
