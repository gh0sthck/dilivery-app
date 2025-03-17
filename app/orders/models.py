from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Model


class Status(Model):
    __tablename__ = "status"
    
    name: Mapped[str] = mapped_column(String(80), nullable=False)


Order = Table(
    "order",
    Model.metadata,
    Column("id", Integer(), primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("user.id")),
    Column("courier_id", ForeignKey("user.id"), nullable=True),
    Column("status", ForeignKey("status.id"))
)
