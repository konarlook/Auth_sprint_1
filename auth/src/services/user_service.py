from sqlalchemy.orm import Session
from sqlalchemy import select

from models.auth_orm_models import UserDataOrm
from schemas.user import CreateUserSchema


def create_user(session: Session, user: CreateUserSchema) -> UserDataOrm:
    db_user = UserDataOrm(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
