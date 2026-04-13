from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.resume import router as resume_router
from .services.database_service import db_service
from contextlib import asynccontextmanager
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connecting to MongoDB...")
    try:
        connected = await asyncio.wait_for(db_service.connect(), timeout=5.0)
        if connected:
            logger.info("✅ Database connected successfully")
    except Exception as e:
        logger.warning(f"❌ Database connection failed: {e}")
    yield
    await db_service.disconnect()

app = FastAPI(title="MatchAI API", lifespan=lifespan)

# Allow Frontend to communicate with Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prefix all routes with /api
app.include_router(resume_router, prefix="/api", tags=["Analysis"])

@app.get("/")
def home():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)