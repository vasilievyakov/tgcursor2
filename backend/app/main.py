"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import channels, posts, export

app = FastAPI(
    title="Telegram Content Parser & Analyzer API",
    description="API for parsing and analyzing Telegram channel content",
    version="0.1.0",
)

# CORS middleware for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(channels.router)
app.include_router(posts.router)
app.include_router(export.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "tgcursor2-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Telegram Content Parser & Analyzer API",
        "version": "0.1.0",
        "docs": "/docs",
    }

