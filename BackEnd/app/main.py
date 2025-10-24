from fastapi import FastAPI
from app.routes import stream
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Register your routers
app.include_router(stream.router, prefix="/api/stream", tags=["Stream"])

@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} backend is running"}
