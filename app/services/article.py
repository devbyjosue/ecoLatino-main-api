from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.repositories.article import ArticleRepository
from app.repositories.source import SourceRepository
from app.schemas.article import ArticleCreate, ArticleUpdate


class ArticleService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ArticleRepository(db)
        self.source_repository = SourceRepository(db)

    async def get_article(self, article_id: int) -> Optional[Article]:
        return await self.repository.get(article_id)

    async def list_articles(self, skip: int = 0, limit: int = 100) -> Sequence[Article]:
        return await self.repository.list(skip=skip, limit=limit)

    async def ingest_article(self, schema: ArticleCreate) -> Article:
        # Verify that the parent Source exists
        source = await self.source_repository.get(schema.source_id)
        if not source:
            raise ValueError(f"Source with ID {schema.source_id} does not exist.")

        # Enforce unique article URL
        existing = await self.repository.get_by_url(str(schema.url))
        if existing:
            raise ValueError(f"Article with URL {schema.url} already exists.")

        return await self.repository.create(schema)

    async def update_article(self, article_id: int, schema: ArticleUpdate) -> Optional[Article]:
        if schema.source_id is not None:
            source = await self.source_repository.get(schema.source_id)
            if not source:
                raise ValueError(f"Source with ID {schema.source_id} does not exist.")

        if schema.url is not None:
            existing = await self.repository.get_by_url(str(schema.url))
            if existing and existing.id != article_id:
                raise ValueError(f"Article with URL {schema.url} already exists.")

        return await self.repository.update(article_id, schema)

    async def delete_article(self, article_id: int) -> bool:
        return await self.repository.delete(article_id)
