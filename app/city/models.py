import typing
from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Model

if typing.TYPE_CHECKING:
    from app.food.models import Shop
    from app.auth.models import User


class City(Model):
    __tablename__ = "city"

    name: Mapped[str] = mapped_column(String(length=80))
    shops: Mapped[List["Shop"]] = relationship("Shop", back_populates="cities")
