from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routes import note_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(note_router, prefix="/api")
    return app

app = create_app()
