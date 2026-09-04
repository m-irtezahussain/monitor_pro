from contextlib import asynccontextmanager
from tortoise.contrib.fastapi import RegisterTortoise
from app.config import TORTOISE_ORM
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app=app,
        config=TORTOISE_ORM,
        add_exception_handlers=True,
    ):
        yield

app = FastAPI(
    title="Monitor Pro API",
    description="FastAPI starter application running in Docker",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Welcome to Monitor Pro FastAPI app!"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
