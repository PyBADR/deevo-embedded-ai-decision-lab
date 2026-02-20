from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, claims, decisions
from app.config import settings
import logging

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
