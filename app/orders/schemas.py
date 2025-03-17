import enum
from typing import Optional
from pydantic import BaseModel


class ERole(enum.Enum):
    CLIENT: int = 0
    ADMINISTRATIOR: int = 1
    COURIER: int = 2 


class EStatus(enum.Enum):
    PENDING: int = 0
    ON_WAY: int = 1 
    DONE: int = 2


class SStatus(BaseModel):
    id: int
    name: str
    

class SOrder(BaseModel):
    # id: int
    user_id: int
    courier_id: Optional[int]
    status: int
