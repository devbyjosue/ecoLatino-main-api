from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.story import Story, StoryArticle
from app.schemas.story import StoryCreate, StoryUpdate


class StoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get(self, story_id: int) -> Optional[Story]:
        result = await self.db.execute(
            select(Story)
            .options(
                selectinload(Story.article_associations).selectinload(StoryArticle.article)
            )
            .where(Story.id == story_id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> Sequence[Story]:
        result = await self.db.execute(
            select(Story)
            .options(
                selectinload(Story.article_associations).selectinload(StoryArticle.article)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, schema: StoryCreate) -> Story:
        db_story = Story(
            title=schema.title,
            summary=schema.summary,
        )
        self.db.add(db_story)
        await self.db.commit()
        await self.db.refresh(db_story)
        return db_story

    async def update(self, story_id: int, schema: StoryUpdate) -> Optional[Story]:
        db_story = await self.get(story_id)
        if not db_story:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_story, field, value)

        await self.db.commit()
        await self.db.refresh(db_story)
        return db_story

    async def delete(self, story_id: int) -> bool:
        db_story = await self.get(story_id)
        if not db_story:
            return False
        await self.db.delete(db_story)
        await self.db.commit()
        return True

    async def assign_article(
        self, story_id: int, article_id: int, confidence_score: float = 1.0
    ) -> Optional[StoryArticle]:
        result = await self.db.execute(
            select(StoryArticle).where(
                StoryArticle.story_id == story_id,
                StoryArticle.article_id == article_id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.confidence_score = confidence_score
            await self.db.commit()
            await self.db.refresh(existing)
            return existing

        db_assoc = StoryArticle(
            story_id=story_id,
            article_id=article_id,
            confidence_score=confidence_score,
        )
        self.db.add(db_assoc)
        await self.db.commit()
        await self.db.refresh(db_assoc)
        return db_assoc

    async def remove_article(self, story_id: int, article_id: int) -> bool:
        result = await self.db.execute(
            select(StoryArticle).where(
                StoryArticle.story_id == story_id,
                StoryArticle.article_id == article_id,
            )
        )
        assoc = result.scalar_one_or_none()
        if not assoc:
            return False
        await self.db.delete(assoc)
        await self.db.commit()
        return True
