from fastapi import APIRouter

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[dict[str, str]])
async def get_sources() -> list[dict[str, str]]:
    """
    Get all sources.
    """
    return []
