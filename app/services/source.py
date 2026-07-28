from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.source import Source
from app.repositories.source import SourceRepository
from app.schemas.source import SourceCreate, SourceUpdate


class SourceService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = SourceRepository(db)

    async def get_source(self, source_id: int) -> Optional[Source]:
        return await self.repository.get(source_id)

    async def list_sources(self, skip: int = 0, limit: int = 100) -> Sequence[Source]:
        return await self.repository.list(skip=skip, limit=limit)

    async def create_source(self, schema: SourceCreate) -> Source:
        existing = await self.repository.get_by_url(str(schema.url))
        if existing:
            raise ValueError(f"Source with URL {schema.url} already exists.")
        return await self.repository.create(schema)

    async def update_source(self, source_id: int, schema: SourceUpdate) -> Optional[Source]:
        if schema.url:
            existing = await self.repository.get_by_url(str(schema.url))
            if existing and existing.id != source_id:
                raise ValueError(f"Source with URL {schema.url} already exists.")
           
        return await self.repository.update(source_id, schema)

    async def delete_source(self, source_id: int) -> bool:
        return await self.repository.delete(source_id)
