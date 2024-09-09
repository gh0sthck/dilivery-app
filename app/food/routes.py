from typing import Dict
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends

from database import get_async_session

food_router = APIRouter(prefix="/food", tags=["Food"])

# FIX ROUTING
@food_router.get("/all/")
async def all_food() -> dict[str, str]:
    return {
        "test_response": "200",
    }
