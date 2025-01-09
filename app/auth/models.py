from typing import List
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.city.models import City
from app.database import Model


class Role(Model):
    __tablename__ = "role"
    
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    users: Mapped[List["Role"]] = relationship("User", back_populates="roles")


class User(Model):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(256), nullable=False)
    password: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    balance: Mapped[float] = mapped_column(default=0.0)
    city: Mapped["City"] = mapped_column(ForeignKey("city.id"))
    order_create: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=True)
    role: Mapped["Role"] = mapped_column(ForeignKey("role.id"))
    roles: Mapped[List["Role"]] = relationship(back_populates="users")
