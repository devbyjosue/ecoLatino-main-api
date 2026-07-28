from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate


class ArticleRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, article_id: int) -> Optional[Article]:
        result = await self.db.execute(
            select(Article).where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    async def get_by_url(self, url: str) -> Optional[Article]:
        result = await self.db.execute(
            select(Article).where(Article.url == url)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> Sequence[Article]:
        result = await self.db.execute(
            select(Article).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, schema: ArticleCreate) -> Article:
        db_article = Article(
            source_id=schema.source_id,
            title=schema.title,
            url=str(schema.url),
            content=schema.content,
            published_at=schema.published_at,
        )
        self.db.add(db_article)
        await self.db.commit()
        await self.db.refresh(db_article)
        return db_article

    async def update(self, article_id: int, schema: ArticleUpdate) -> Optional[Article]:
        db_article = await self.get(article_id)
        if not db_article:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "url" and value is not None:
                setattr(db_article, field, str(value))
            else:
                setattr(db_article, field, value)

        await self.db.commit()
        await self.db.refresh(db_article)
        return db_article

    async def delete(self, article_id: int) -> bool:
        db_article = await self.get(article_id)
        if not db_article:
            return False
        await self.db.delete(db_article)
        await self.db.commit()
        return True
