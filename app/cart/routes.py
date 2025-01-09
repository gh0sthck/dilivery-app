from typing import Annotated, List, Optional
from fastapi import Depends
from fastapi.routing import APIRouter

from app.cart.cart_explorer import CartExplorer
from app.cart.schemas import SCart

cart_router = APIRouter(prefix="/api/cart", tags=["Cart"])
cart_explorer = CartExplorer()


@cart_router.get("/all/")
async def cart_all() -> Optional[List[SCart]]:
    return await cart_explorer.get()


@cart_router.get("/{id}/")
async def cart_by_id(id: int) -> Optional[SCart]:
    return await cart_explorer.get(id=id)


@cart_router.post("/add/")
async def cart_add(schema: Annotated[SCart, Depends()]) -> Optional[SCart]:
    return await cart_explorer.post(schema=schema)
