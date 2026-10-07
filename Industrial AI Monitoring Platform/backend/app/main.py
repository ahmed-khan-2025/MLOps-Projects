from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.ml_model import load_model
from app.routers import health, machines, predictions
from app.websocket_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    load_model()
    yield


app = FastAPI(
    title="Industrial AI Monitoring Platform",
    description="Full-stack Industrial AI platform using Python, FastAPI, TypeScript, React, PostgreSQL and ML.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(machines.router)
app.include_router(predictions.router)


@app.get("/")
def root():
    return {
        "application": "Industrial AI Monitoring Platform",
        "status": "running",
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)