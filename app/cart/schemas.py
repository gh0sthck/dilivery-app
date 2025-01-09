from pydantic import BaseModel


class SCart(BaseModel):
    id: int
    user_id: int
    food_id: int
