import uuid
import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey

from models.base import Base, str_50, str_256, intpk, uuidpk, datetime_at_utc


class UsersOrm(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "Таблица пользователь - роль"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_data.id"), primary_key=True, comment="ID пользователя"
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="ID роли")


class RolesOrm(Base):
    __tablename__ = "roles"
    __table_args__ = {"comment": "Таблица ролей"}

    id: Mapped[intpk]
    role_name: Mapped[str_50] = mapped_column(comment="Название роли")
    comment: Mapped[str_256] = mapped_column(
        comment="Комментарий к роли", nullable=True
    )


class MixActionsOrm(Base):
    __tablename__ = "mix_actions"
    __table_args__ = {"comment": "Таблица привыязки действий к ролям"}

    id: Mapped[intpk]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="ID роли")
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id"), comment="ID действия"
    )


class ActionsOrm(Base):
    __tablename__ = "actions"
    __table_args__ = {"comment": "Таблица действий"}

    id: Mapped[intpk]
    action_name: Mapped[str_50] = mapped_column(comment="Название действия")
    comment: Mapped[str_256] = mapped_column(
        comment="Комментарий к действию", nullable=True
    )


class UserDataOrm(Base):
    __tablename__ = "user_data"
    __table_args__ = (
        UniqueConstraint("user_name"),
        UniqueConstraint("email"),
        {"comment": "Таблица данных пользователя"},
    )

    id: Mapped[uuidpk]
    user_name: Mapped[str_50] = mapped_column(
        comment="Имя пользователя", unique=True, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column(
        comment="Хэш пароля пользователя", nullable=False
    )
    first_name: Mapped[str_50] = mapped_column(
        comment="Имя пользователя", nullable=True
    )
    last_name: Mapped[str_50] = mapped_column(
        comment="Фамилия пользователя", nullable=True
    )
    email: Mapped[str_256] = mapped_column(
        comment="Электронная почта пользователя", nullable=False, unique=True
    )
    register_date: Mapped[datetime_at_utc] = mapped_column(
        comment="Дата регистрации пользователя", nullable=False
    )
    phone_number: Mapped[str_50] = mapped_column(
        comment="Номер телефона пользователя", nullable=True
    )


class AuthHistotyOrm(Base):
    __tablename__ = "auth_history"
    __table_args__ = {"comment": "Таблица истории авторизации"}

    id: Mapped[intpk]
    dt_login: Mapped[datetime_at_utc] = mapped_column(
        comment="Дата авторизации пользователя", nullable=False
    )
    dt_logout: Mapped[datetime.datetime] = mapped_column(
        comment="Дата logout пользователя", nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_data.id"), comment="ID пользователя"
    )
    device_id: Mapped[int] = mapped_column(comment="ID устройства", nullable=True)
