from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ArticleBase(BaseModel):
    title: str = Field(..., max_length=512)
    url: HttpUrl
    content: str
    published_at: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    source_id: int


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=512)
    url: Optional[HttpUrl] = None
    content: Optional[str] = None
    published_at: Optional[datetime] = None
    source_id: Optional[int] = None


class ArticleResponse(ArticleBase):
    id: int
    source_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
