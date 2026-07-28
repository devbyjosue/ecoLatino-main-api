from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=dict[str, str])
async def live() -> dict[str, str]:
    """
    Liveness check endpoint.
    """
    return {"status": "ok"}


@router.get("/ready", response_model=dict[str, str])
async def ready() -> dict[str, str]:
    """
    Readiness check endpoint.
    """
    return {"status": "ok"}
