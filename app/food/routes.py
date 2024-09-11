from typing import Dict
from fastapi import APIRouter

food_router = APIRouter(prefix="/food", tags=["Food"])


@food_router.get("/all/")
async def all_food() -> Dict[str, str]:
    return {
        "test_response": "200",
    }
