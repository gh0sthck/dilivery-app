import uvicorn
from fastapi import FastAPI

from app.settings import config
from app.food import food_router

app = FastAPI(
    debug=config.debug,
    title=config.name,
    version=config.version,
    docs_url=config.docs_url,
)


app.include_router(food_router)
