from typing import Optional
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str


class CategorySchemaRead(CategorySchema):
    id: int


class ShopSchema(BaseModel):
    rate: float
    city: int
    name: str = Field(max_length=90)


class ShopSchemaRead(ShopSchema):
    id: int


class FoodSchema(BaseModel):
    name: str = Field(max_length=80)
    rate: float 
    description: str
    price: int
    shop: int
    category: Optional[int]


class FoodSchemaRead(FoodSchema): 
    id: int
