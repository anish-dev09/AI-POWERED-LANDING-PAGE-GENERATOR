"""
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db
from app.api.routers import business, landing_page, health


# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and perform startup/shutdown tasks."""
    print("🚀 Starting AI Landing Page Generator API...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
    yield
    print("👋 Shutting down AI Landing Page Generator API...")


# Create FastAPI application
app = FastAPI(
    title="AI Landing Page Generator API",
    description="AI-powered landing page generation service with Google Gemini and OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Landing Page Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "businesses": "/api/v1/businesses",
            "landing_pages": "/api/v1/landing-pages",
            "health": "/api/v1/health"
        }
    }


# Include routers with API versioning
app.include_router(health.router, prefix="/api/v1")
app.include_router(business.router, prefix="/api/v1")
app.include_router(landing_page.router, prefix="/api/v1")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )


# Main entry point for running the server
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 AI LANDING PAGE GENERATOR API")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
