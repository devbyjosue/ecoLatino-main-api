from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=dict[str, int])
async def get_analytics() -> dict[str, int]:
    """
    Get analytics summary.
    """
    return {}
