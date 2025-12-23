from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth, students, teachers, instruments, schedule
from backend.app.data.db import engine, Base
from backend.app.data import models


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Музыкальная школа API",
    description="API для управления учениками, преподавателями, инструментами и расписанием",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(instruments.router)
app.include_router(schedule.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
