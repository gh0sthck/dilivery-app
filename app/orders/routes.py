from typing import Annotated, List, Optional
from fastapi import Depends
from fastapi.routing import APIRouter

from app.db_explorer import DbExplorer
from app.orders.models import Order
from app.orders.order_explorer import OrderExplorer
from app.orders.schemas import OrderSchema

order_router = APIRouter(prefix="/api/orders", tags=["Orders"])
order_explorer = OrderExplorer()


@order_router.get("/all/")
async def orders_all() -> Optional[List[OrderSchema]]:
    return await order_explorer.get()


@order_router.get("/{id}/")
async def order_by_id(id: int) -> Optional[OrderSchema]:
    return await order_explorer.get(id=id)


@order_router.post("/add/")
async def orders_add(schema: Annotated[OrderSchema, Depends()]) -> Optional[OrderSchema]:
    return await order_explorer.post(schema=schema)
