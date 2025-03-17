from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.auth.routes import get_current_user
from app.auth.schemas import SUser
from app.cart.cart_explorer import CartExplorer
from app.cart.schemas import SCart, SCartAdd
from app.cart.utils import change_create_status
from app.orders.routes import orders_explorer
from app.orders.schemas import EStatus, SOrder

cart_router = APIRouter(prefix="/api/cart", tags=["Cart"])
cart_explorer = CartExplorer()


@cart_router.get("/all/")
async def cart_all() -> Optional[List[SCart]]:
    return await cart_explorer.get()


@cart_router.get("/{id}/")
async def cart_by_id(id: int) -> Optional[SCart]:
    return await cart_explorer.get(id=id)


@cart_router.post("/add/")
async def cart_add(
    schema: Annotated[SCartAdd, Depends()],
    current_user: SUser = Depends(get_current_user),
) -> Optional[SCart]:
    if not current_user.order_create:
        schema_dump = schema.model_dump()
        schema_dump["user_id"] = current_user.id
        schema = SCart.model_validate(schema_dump)
        return await cart_explorer.post(schema=schema)
    raise HTTPException(status_code=403, detail={"detail": "You already have order."})


@cart_router.post("/confirm/")
async def cart_confirm(client: SUser = Depends(get_current_user)) -> SOrder:
    if not client.order_create:
        await change_create_status(client.id)
        order = SOrder(user_id=client.id, courier_id=None, status=EStatus.PENDING.value)
        await orders_explorer.post(order)
        return order
    raise HTTPException(status_code=403, detail={"detail": "You already have order."})
