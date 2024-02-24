import uuid
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey

from models.base import Base, str_50, str_256, intpk, uuidpk, datetime_at_utc


class UsersOrm(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "Таблица пользователь - роль"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_data.id"), primary_key=True, comment="ID пользователя"
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="ID роли")

    role: Mapped["RolesOrm"] = relationship(back_populates="roles")
    user: Mapped["UserDataOrm"] = relationship(back_populates="users")


class RolesOrm(Base):
    __tablename__ = "roles"
    __table_args__ = {"comment": "Таблица ролей"}

    id: Mapped[intpk]
    role_name: Mapped[str_50] = mapped_column(comment="Название роли")
    comment: Mapped[str_256] = mapped_column(comment="Комментарий к3 роли")

    user: Mapped["UsersOrm"] = relationship(back_populates="users")
    actions: Mapped["MixActionsOrm"] = relationship(back_populates="role")


class MixActionsOrm(Base):
    __tablename__ = "mix_actions"
    __table_args__ = {"comment": "Таблица привыязки действий к ролям"}

    id: Mapped[intpk]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), comment="ID роли")
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id"), comment="ID действия"
    )

    roles: Mapped[List["RolesOrm"]] = relationship(back_populates="roles")
    actions: Mapped[List["ActionsOrm"]] = relationship(back_populates="actions")


class ActionsOrm(Base):
    __tablename__ = "actions"
    __table_args__ = {"comment": "Таблица действий"}

    id: Mapped[intpk]
    action_name: Mapped[str_50] = mapped_column(comment="Название действия")
    comment: Mapped[str_256] = mapped_column(comment="Комментарий к действию")

    actions: Mapped["MixActionsOrm"] = relationship(back_populates="mix_actions")


class UserDataOrm(Base):
    __tablename__ = "user_data"
    __table_args__ = (
        UniqueConstraint("user_name"),
        UniqueConstraint("email"),
        {"comment": "Таблица данных пользователя"},
    )

    id: Mapped[uuidpk]
    user_name: Mapped[str_50] = mapped_column(comment="Имя пользователя", unique=True)
    hashed_password: Mapped[str] = mapped_column(
        comment="Хэш пароля пользователя", nullable=False
    )
    first_name: Mapped[str_50] = mapped_column(comment="Имя пользователя")
    last_name: Mapped[str_50] = mapped_column(comment="Фамилия пользователя")
    email: Mapped[str_256] = mapped_column(
        comment="Электронная почта пользователя", nullable=False, unique=True
    )
    register_date: Mapped[datetime_at_utc] = mapped_column(
        comment="Дата регистрации пользователя", nullable=False
    )
    phone_number: Mapped[str_50] = mapped_column(comment="Номер телефона пользователя")

    users: Mapped["UsersOrm"] = relationship(back_populates="user")
    auth_history: Mapped[List["AuthHistotyOrm"]] = relationship(back_populates="user")


class AuthHistotyOrm(Base):
    __tablename__ = "auth_history"
    __table_args__ = {"comment": "Таблица истории авторизации"}

    id: Mapped[intpk]
    dt_login: Mapped[datetime_at_utc] = mapped_column(
        comment="Дата авторизации пользователя", nullable=False
    )
    login_date: Mapped[datetime_at_utc] = mapped_column(
        comment="Дата авторизации пользователя", nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_data.id"), comment="ID пользователя"
    )
    device_id: Mapped[int] = mapped_column(comment="ID устройства")

    user: Mapped["UserDataOrm"] = relationship(back_populates="user_data")