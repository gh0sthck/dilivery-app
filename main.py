from fastapi import FastAPI

from app.settings import config
from app.food import food_router, shop_router, category_router
from app.city import city_router
from app.auth import users_router
from app.cart import cart_router
from app.orders import orders_router

app = FastAPI(
    debug=config.debug,
    title=config.name,
    version=config.version,
    docs_url=config.docs_url,
)

app.include_router(food_router)
app.include_router(shop_router)
app.include_router(city_router)
app.include_router(users_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(orders_router)
