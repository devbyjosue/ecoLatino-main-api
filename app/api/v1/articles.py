from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_article_service
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.services.article import ArticleService

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def ingest_article(
    schema: ArticleCreate,
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    try:
        article = await service.ingest_article(schema)
        return ArticleResponse.model_validate(article)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[ArticleResponse])
async def list_articles(
    skip: int = 0,
    limit: int = 100,
    service: ArticleService = Depends(get_article_service),
) -> list[ArticleResponse]:
    articles = await service.list_articles(skip=skip, limit=limit)
    return [ArticleResponse.model_validate(a) for a in articles]


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    article = await service.get_article(article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID {article_id} not found",
        )
    return ArticleResponse.model_validate(article)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    schema: ArticleUpdate,
    service: ArticleService = Depends(get_article_service),
) -> ArticleResponse:
    try:
        article = await service.update_article(article_id, schema)
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Article with ID {article_id} not found",
            )
        return ArticleResponse.model_validate(article)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    service: ArticleService = Depends(get_article_service),
) -> None:
    deleted = await service.delete_article(article_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID {article_id} not found",
        )
