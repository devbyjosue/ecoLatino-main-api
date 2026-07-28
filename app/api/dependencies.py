from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.source import SourceService
from app.services.article import ArticleService
from app.services.story import StoryService
from app.services.crawl_job import CrawlJobService


async def get_source_service(
    db: AsyncSession = Depends(get_db),
) -> SourceService:
    return SourceService(db)


async def get_article_service(
    db: AsyncSession = Depends(get_db),
) -> ArticleService:
    return ArticleService(db)


async def get_story_service(
    db: AsyncSession = Depends(get_db),
) -> StoryService:
    return StoryService(db)


async def get_crawl_job_service(
    db: AsyncSession = Depends(get_db),
) -> CrawlJobService:
    return CrawlJobService(db)
