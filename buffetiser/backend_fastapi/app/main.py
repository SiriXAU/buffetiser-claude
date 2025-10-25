"""
Main FastAPI application.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api.endpoints import (
    dividends,
    exports,
    investments,
    portfolio,
    tax,
    transactions,
    updates,
)
from app.config import get_settings
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    await init_db()

    # Initialize Redis cache
    redis = aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="buffetiser-cache")

    yield

    # Shutdown
    await redis.close()


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    investments.router,
    prefix=f"{settings.API_V1_PREFIX}/investments",
    tags=["investments"]
)
app.include_router(
    transactions.router,
    prefix=f"{settings.API_V1_PREFIX}/transactions",
    tags=["transactions"]
)
app.include_router(
    dividends.router,
    prefix=f"{settings.API_V1_PREFIX}/dividends",
    tags=["dividends"]
)
app.include_router(
    portfolio.router,
    prefix=f"{settings.API_V1_PREFIX}/portfolio",
    tags=["portfolio"]
)
app.include_router(
    tax.router,
    prefix=f"{settings.API_V1_PREFIX}/tax",
    tags=["tax"]
)
app.include_router(
    exports.router,
    prefix=f"{settings.API_V1_PREFIX}/export",
    tags=["exports"]
)
app.include_router(
    updates.router,
    prefix=f"{settings.API_V1_PREFIX}/updates",
    tags=["updates"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Buffetiser API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
