from pydantic import BaseModel


class Order:
    id: int
    user_id: int
    product_id: int
