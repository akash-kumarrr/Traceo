from fastapi import FastAPI
from contextlib import asynccontextmanager

from models.base import Base
from core.database import engine

from api.routes.user import router as user_router
from api.routes.health import router as health_router

@asynccontextmanager
async def lifespan(app : FastAPI)  :
    print("starting with return code 0")
    Base.metadata.create_all(bind=engine)
    yield 
    print("backed terminated with return code 0")


app = FastAPI(
    title="traceo-backend",
    description="traceo backend system",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "app" : "taceo-backend"
    }

app.include_router(health_router)
app.include_router(user_router)