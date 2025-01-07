from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Model


Order = Table(
    "order",
    Model.metadata,
    Column("id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("user.id")),
    Column("food_id", ForeignKey("food.id")),
)
