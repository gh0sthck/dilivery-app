from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Model


class Order(Model):
    __tablename__ = "order"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) 
    product_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    
