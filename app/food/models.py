from typing import List
from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.city.models import City
from app.database import Model


class Category(Model):
    __tablename__ = "category"
    
    name: Mapped[str] = mapped_column(String(length=80)) 
    food: Mapped[List["Food"]] = relationship(back_populates="categories")


class Shop(Model):
    __tablename__ = "shop"

    name: Mapped[str] = mapped_column(String(length=80))
    rate: Mapped[float] = mapped_column(Float(precision=2), default=0.0) 
    city: Mapped["City"] = mapped_column(ForeignKey("city.id"))
    cities: Mapped[List["City"]] = relationship(back_populates="shops")
    food: Mapped[List["Food"]] = relationship(back_populates="shops")


class Food(Model):
    __tablename__ = "food"

    name: Mapped[str] = mapped_column(String(length=80))
    rate: Mapped[float] = mapped_column(Float(precision=2), default=0.0)
    description: Mapped[str | None] = mapped_column(default=None)
    price: Mapped[int]
    shop: Mapped["Shop"] = mapped_column(ForeignKey("shop.id"))
    category: Mapped["Category"] = mapped_column(ForeignKey("category.id"), nullable=True)
    shops: Mapped[List["Shop"]] = relationship(back_populates="food")
    categories: Mapped[List["Category"]] = relationship(back_populates="food")
