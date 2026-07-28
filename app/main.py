from fastapi import FastAPI

from app.api.v1 import router as api_v1_router
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Register health check routes under root (/health/live, /health/ready)
app.include_router(health_router)

# Register API v1 routes (/api/v1/...)
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
