"""
Main FastAPI application file.
Configures the application, includes routers, and creates database tables.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from database.config import engine, Base
from controllers.auth_controller import router as auth_router
from controllers.post_controller import router as post_router

# Create database tables (optional for demonstration)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️  Warning: Database connection error: {e}")
    print("⚠️  API will start, but database functions won't work")
    print("⚠️  For full functionality, configure MySQL connection")

# Create FastAPI application
app = FastAPI(
    title="Social Media API",
    description="""
    FastAPI application with MVC architecture for social media.
    
    ## Features
    
    * **Authentication**: Registration and authorization with JWT tokens
    * **Posts**: Create, retrieve, and delete posts
    * **Caching**: Automatic post caching for 5 minutes
    * **Validation**: Complete data validation through Pydantic
    * **Security**: Token-based authentication with dependency injection
    
    ## Technologies
    
    * FastAPI with async support
    * SQLAlchemy ORM with MySQL/SQLite
    * JWT authentication
    * Pydantic validation
    * TTL caching
    * MVC architecture
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@socialmediaapi.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # In production, should be limited to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(post_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root API endpoint.

    Returns:
        dict: Information about API and available endpoints
    """
    return {
        "message": "Social Media API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": {
                "signup": "POST /auth/signup",
                "login": "POST /auth/login",
            },
            "posts": {
                "create": "POST /posts/",
                "get_all": "GET /posts/",
                "delete": "DELETE /posts/{post_id}",
                "stats": "GET /posts/stats",
            },
        },
        "features": [
            "JWT Authentication",
            "1MB Payload Validation",
            "5-minute Response Caching",
            "MVC Architecture",
            "Dependency Injection",
            "Comprehensive Documentation",
        ],
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    API health check endpoint.

    Returns:
        dict: Service and database status
    """
    try:
        # Check database connection
        from database.config import SessionLocal

        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        database_status = "connected"
    except Exception as e:
        database_status = "disconnected: connect MySQL for full functionality"

    return {
        "status": "healthy",
        "database": database_status,
        "cache": "active",
        "api": "running",
    }


# Global error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global error handler for unhandled exceptions."""
    return {
        "error": "Internal server error",
        "detail": "Please try again later",
        "status_code": 500,
    }


if __name__ == "__main__":
    # Run development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on changes
        log_level="info",
    )
