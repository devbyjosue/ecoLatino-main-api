from fastapi import APIRouter

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[dict[str, str]])
async def get_articles() -> list[dict[str, str]]:
    """
    Get all articles.
    """
    return []
