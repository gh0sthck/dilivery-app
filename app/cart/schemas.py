from pydantic import BaseModel


class SCart(BaseModel):
    id: int
    user_id: int
    food_id: int


class SCartAdd(BaseModel):
    id: int
    food_id: int
