from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.auth.routes import get_current_user
from app.auth.schemas import SUser
from app.db_explorer import DbExplorer
from app.orders.models import Status
from app.orders.order_explorer import OrderExplorer
from app.orders.schemas import ERole, EStatus, SOrder, SStatus
from app.orders.utils import change_order_status

orders_router = APIRouter(prefix="/api/orders", tags=["Orders"])
orders_explorer = OrderExplorer()
status_explorer = DbExplorer(Status, SStatus)


@orders_router.get("/status_all/")
async def status_all() -> Optional[List[SStatus]]:
    return await status_explorer.get()


@orders_router.post("/status_add/")
async def status_add(schema: Annotated[SStatus, Depends()]) -> SStatus:
    return await status_explorer.post(schema=schema)



@orders_router.get("/all/")
async def orders_all() -> Optional[List[SOrder]]:
    return await orders_explorer.get()


@orders_router.get("/{id}/")
async def orders_by_id(id: int) -> Optional[SOrder]:
    return await orders_explorer.get(id=id)


@orders_router.post("/add/")
async def orders_add(schema: Annotated[SOrder, Depends()]) -> Optional[SOrder]:
    return await orders_explorer.post(schema=schema)


@orders_router.post("/accept/{order_id}")
async def orders_accept(order_id: int, current_user: SUser = Depends(get_current_user)) -> None:
    if current_user.role >= ERole.ADMINISTRATIOR.value:
        return await change_order_status(order_id, EStatus.ON_WAY.value) 
    raise HTTPException(status_code=403, detail={"detail": "You're not a Delivery man."})


@orders_router.post("/confirm/{order_id}")
async def orders_confirm(order_id: int, current_user: SUser = Depends(get_current_user)) -> SOrder:
    if current_user.role >= ERole.ADMINISTRATIOR.value:
        return await change_order_status(order_id, EStatus.DONE.value)
    raise HTTPException(status_code=403, detail={"detail": "You're not Delivery man."})
