from fastapi import FastAPI
from sqlalchemy import text

from async_database import AsyncSessionLocal

app = FastAPI(title="Async Course API")


@app.get("/")
async def home():
    return {"message": "Async FastAPI is running"}


@app.get("/health")
async def health_check():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": result.scalar()
        }