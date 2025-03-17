from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Model


class ModelTest(Model):
    __tablename__ = "testmodel"
    value: Mapped[str] = mapped_column(String(length=80))


class ModelTestS(BaseModel):
    id: int
    value: str
