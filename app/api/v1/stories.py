from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_story_service
from app.schemas.story import (
    StoryCreate,
    StoryDetailResponse,
    StoryResponse,
    StoryUpdate,
    StoryArticleAssign,
    StoryArticleResponse,
)
from app.services.story import StoryService

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def create_story(
    schema: StoryCreate,
    service: StoryService = Depends(get_story_service),
) -> StoryResponse:
    story = await service.create_story(schema)
    return StoryResponse.model_validate(story)


@router.get("", response_model=list[StoryResponse])
async def list_stories(
    skip: int = 0,
    limit: int = 100,
    service: StoryService = Depends(get_story_service),
) -> list[StoryResponse]:
    stories = await service.list_stories(skip=skip, limit=limit)
    return [StoryResponse.model_validate(s) for s in stories]


@router.get("/{story_id}", response_model=StoryDetailResponse)
async def get_story(
    story_id: int,
    service: StoryService = Depends(get_story_service),
) -> StoryDetailResponse:
    story = await service.get_story(story_id)
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found",
        )
    return StoryDetailResponse.model_validate(story)


@router.put("/{story_id}", response_model=StoryResponse)
async def update_story(
    story_id: int,
    schema: StoryUpdate,
    service: StoryService = Depends(get_story_service),
) -> StoryResponse:
    story = await service.update_story(story_id, schema)
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found",
        )
    return StoryResponse.model_validate(story)


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(
    story_id: int,
    service: StoryService = Depends(get_story_service),
) -> None:
    deleted = await service.delete_story(story_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found",
        )


@router.post("/{story_id}/articles", response_model=StoryArticleResponse)
async def assign_article(
    story_id: int,
    assign_schema: StoryArticleAssign,
    service: StoryService = Depends(get_story_service),
) -> StoryArticleResponse:
    try:
        assoc = await service.assign_article_to_story(
            story_id, assign_schema.article_id, assign_schema.confidence_score
        )
        return StoryArticleResponse.model_validate(assoc)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{story_id}/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_article(
    story_id: int,
    article_id: int,
    service: StoryService = Depends(get_story_service),
) -> None:
    try:
        removed = await service.remove_article_from_story(story_id, article_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Association between story {story_id} and article {article_id} not found",
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
