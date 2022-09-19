from typing import Union, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.schemas.user_schema import UserCreateSchema, UserBase
from app.models.user import User


class UserCRUD:
    # TODO: Сделать базовый CRUD для всех моделек
    # TODO: на основе Generic и наследоваться от него
    @staticmethod
    def create_user(db: Session, obj_in: UserCreateSchema) -> User:
        user_data = jsonable_encoder(obj_in)
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(
            db: Session,
            obj_in: Union[UserCreateSchema, dict],
            db_user: User
    ) -> User:
        user_data = jsonable_encoder(db_user)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in user_data:
            if field in update_data:
                setattr(db_user, field, update_data[field])
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, obj_in: UserBase) -> Optional[User]:
        return db.query(User).filter(
            User.phone_number == obj_in.phone_number
        ).first()

    @staticmethod
    def remove_user(db: Session, db_user: User) -> User:
        db.delete(db_user)
        db.commit()
        return db_user
