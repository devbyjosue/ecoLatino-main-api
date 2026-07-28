from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crawl_job import CrawlJob
from app.schemas.crawl_job import CrawlJobCreate, CrawlJobUpdate


class CrawlJobRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, job_id: int) -> Optional[CrawlJob]:
        result = await self.db.execute(
            select(CrawlJob).where(CrawlJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> Sequence[CrawlJob]:
        result = await self.db.execute(
            select(CrawlJob).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def list_by_source(self, source_id: int, skip: int = 0, limit: int = 100) -> Sequence[CrawlJob]:
        result = await self.db.execute(
            select(CrawlJob)
            .where(CrawlJob.source_id == source_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, schema: CrawlJobCreate) -> CrawlJob:
        db_job = CrawlJob(
            source_id=schema.source_id,
        )
        self.db.add(db_job)
        await self.db.commit()
        await self.db.refresh(db_job)
        return db_job

    async def update(self, job_id: int, schema: CrawlJobUpdate) -> Optional[CrawlJob]:
        db_job = await self.get(job_id)
        if not db_job:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_job, field, value)

        await self.db.commit()
        await self.db.refresh(db_job)
        return db_job

    async def delete(self, job_id: int) -> bool:
        db_job = await self.get(job_id)
        if not db_job:
            return False
        await self.db.delete(db_job)
        await self.db.commit()
        return True
