from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import health, claims, decisions
from app.config import settings
from app.utils.logging import get_trace_id, set_trace_id, get_logger
import logging
import uuid

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = get_logger(__name__)

app = FastAPI(
    title="DEEVO Intelligence Lab API",
    description="Insurance Claims Scoring & Decision Intelligence",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def trace_id_middleware(request: Request, call_next):
    """Inject trace_id for every request."""
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    set_trace_id(trace_id)
    
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with trace_id."""
    trace_id = get_trace_id()
    
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "trace_id": trace_id,
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "trace_id": trace_id,
            "path": str(request.url.path)
        }
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """404 handler with trace_id."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Not found",
            "trace_id": get_trace_id(),
            "path": str(request.url.path)
        }
    )


# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(claims.router, tags=["Claims"])
app.include_router(decisions.router, tags=["Decisions"])


@app.get("/")
async def root():
    return {
        "service": "DEEVO Intelligence Lab",
        "version": "1.0.0",
        "docs": "/docs"
    }
