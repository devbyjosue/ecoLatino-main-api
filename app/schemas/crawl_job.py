from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.enums import CrawlJobStatus


class CrawlJobBase(BaseModel):
    source_id: int


class CrawlJobCreate(CrawlJobBase):
    pass


class CrawlJobUpdate(BaseModel):
    status: Optional[CrawlJobStatus] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    items_crawled: Optional[int] = None


class CrawlJobResponse(CrawlJobBase):
    id: int
    status: CrawlJobStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    items_crawled: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
