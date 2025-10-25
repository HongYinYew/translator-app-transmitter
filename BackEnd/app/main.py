from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.routes import stream
from app.core.config import settings
import os
import tempfile
import ffmpeg

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, limit to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register your routers
app.include_router(stream.router, prefix="/api/stream", tags=["Stream"])

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} backend is running"}
