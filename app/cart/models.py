from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Model


Cart = Table(
    "cart",
    Model.metadata,
    Column("id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("user.id")),
    Column("food_id", ForeignKey("food.id")),
)
