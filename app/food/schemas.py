from pydantic import BaseModel, Field


class ShopSchema(BaseModel):
    id: int
    rate: float
    city: int
    name: str = Field(max_length=90)


class FoodSchema(BaseModel):
    id: int
    name: str = Field(max_length=80)
    rate: float 
    description: str
    price: int
    shop: int
