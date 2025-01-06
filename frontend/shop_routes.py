from fastapi import Depends, Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from app.food.routes import food_all
from .utils import Context

frontend_shop_router = APIRouter(prefix="/shop", tags=["Frontend-Shop"])

templates = Jinja2Templates(directory="frontend/templates")


@frontend_shop_router.get("/")
async def main_page(request: Request):
    ctx = Context()
    return templates.TemplateResponse(request=request, name="main.html", context=ctx.get_context)


@frontend_shop_router.get("/all/")
async def all_food_page(request: Request, all_food = Depends(food_all)):
    ctx = Context(foods=all_food)
    return templates.TemplateResponse(request=request, name="shop.html", context=ctx.get_context)
