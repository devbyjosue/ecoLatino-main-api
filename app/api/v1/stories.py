from fastapi import APIRouter

router = APIRouter(prefix="/stories", tags=["stories"])


@router.get("", response_model=list[dict[str, str]])
async def get_stories() -> list[dict[str, str]]:
    """
    Get all stories.
    """
    return []
