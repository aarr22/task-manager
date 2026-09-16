from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import init_db
from app.routers import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}
