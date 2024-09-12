from pydantic import BaseModel, Field


class CitySchema(BaseModel):
    id: int
    name: str = Field(max_length=80)
