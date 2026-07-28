from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crawl_job import CrawlJob
from app.repositories.crawl_job import CrawlJobRepository
from app.repositories.source import SourceRepository
from app.schemas.crawl_job import CrawlJobCreate, CrawlJobUpdate


class CrawlJobService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = CrawlJobRepository(db)
        self.source_repository = SourceRepository(db)

    async def get_job(self, job_id: int) -> Optional[CrawlJob]:
        return await self.repository.get(job_id)

    async def list_jobs(self, skip: int = 0, limit: int = 100) -> Sequence[CrawlJob]:
        return await self.repository.list(skip=skip, limit=limit)

    async def list_jobs_by_source(
        self, source_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[CrawlJob]:
        source = await self.source_repository.get(source_id)
        if not source:
            raise ValueError(f"Source with ID {source_id} does not exist.")
        return await self.repository.list_by_source(source_id, skip=skip, limit=limit)

    async def create_job(self, schema: CrawlJobCreate) -> CrawlJob:
        source = await self.source_repository.get(schema.source_id)
        if not source:
            raise ValueError(f"Source with ID {schema.source_id} does not exist.")
        return await self.repository.create(schema)

    async def update_job(self, job_id: int, schema: CrawlJobUpdate) -> Optional[CrawlJob]:
        return await self.repository.update(job_id, schema)

    async def delete_job(self, job_id: int) -> bool:
        return await self.repository.delete(job_id)
