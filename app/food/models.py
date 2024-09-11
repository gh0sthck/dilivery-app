from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Model


class Shop(Model):
    __tablename__ = "shop"

    name: Mapped[str] = mapped_column(String(length=80))
    food: Mapped[List["Food"]] = relationship(back_populates="shops")


class Food(Model):
    __tablename__ = "food"

    name: Mapped[str] = mapped_column(String(length=80))
    description: Mapped[str]
    price: Mapped[int]
    shop: Mapped["Shop"] = mapped_column(ForeignKey("shop.id"))
    shops: Mapped[List["Shop"]] = relationship(back_populates="food")
