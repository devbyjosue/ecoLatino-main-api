from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.article import ArticleResponse


class StoryArticleResponse(BaseModel):
    article_id: int
    confidence_score: float
    assigned_at: datetime
    article: ArticleResponse

    model_config = ConfigDict(from_attributes=True)


class StoryBase(BaseModel):
    title: str = Field(..., max_length=512)
    summary: str


class StoryCreate(StoryBase):
    pass


class StoryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=512)
    summary: Optional[str] = None


class StoryResponse(StoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Story with nested articles and their relationship metadata
class StoryDetailResponse(StoryResponse):
    article_associations: list[StoryArticleResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Request schema to assign an article to a story
class StoryArticleAssign(BaseModel):
    article_id: int
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
