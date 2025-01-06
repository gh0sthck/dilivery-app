from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.settings import config
from app.food import food_router, shop_router
from app.city import city_router
from app.auth import users_router
from frontend.shop_routes import frontend_shop_router
from frontend.auth_routes import frontend_auth_router

app = FastAPI(
    debug=config.debug,
    title=config.name,
    version=config.version,
    docs_url=config.docs_url,
)

app.mount("/static", StaticFiles(directory="static"), "static")

app.include_router(food_router)
app.include_router(shop_router)
app.include_router(city_router)
app.include_router(users_router)

app.include_router(frontend_shop_router)
app.include_router(frontend_auth_router)
