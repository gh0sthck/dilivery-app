import uvicorn
from fastapi import FastAPI

from settings import config

app = FastAPI(
   debug=config.debug,
   title=config.name,
   version=config.version  
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", reload=True)
