from pydantic import BaseModel, Field


class CitySchema(BaseModel):
    name: str = Field(max_length=80)


class CitySchemaRead(CitySchema):
    id: int
