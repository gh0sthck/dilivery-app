import uvicorn
from fastapi import FastAPI

from settings import config
from food import food_router

app = FastAPI(
   debug=config.debug,
   title=config.name,
   version=config.version,
   docs_url=config.docs_url, 
)

if __name__ == "__main__":
    app.include_router(food_router) # check food/routes.py 
    uvicorn.run(app="main:app", host="127.0.0.1", reload=True)
