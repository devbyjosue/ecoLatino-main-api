from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.story import Story, StoryArticle
from app.repositories.story import StoryRepository
from app.repositories.article import ArticleRepository
from app.schemas.story import StoryCreate, StoryUpdate


class StoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = StoryRepository(db)
        self.article_repository = ArticleRepository(db)

    async def get_story(self, story_id: int) -> Optional[Story]:
        return await self.repository.get(story_id)

    async def list_stories(self, skip: int = 0, limit: int = 100) -> Sequence[Story]:
        return await self.repository.list(skip=skip, limit=limit)

    async def create_story(self, schema: StoryCreate) -> Story:
        return await self.repository.create(schema)

    async def update_story(self, story_id: int, schema: StoryUpdate) -> Optional[Story]:
        return await self.repository.update(story_id, schema)

    async def delete_story(self, story_id: int) -> bool:
        return await self.repository.delete(story_id)

    async def assign_article_to_story(
        self, story_id: int, article_id: int, confidence_score: float = 1.0
    ) -> StoryArticle:
        # Check if story exists
        story = await self.repository.get(story_id)
        if not story:
            raise ValueError(f"Story with ID {story_id} does not exist.")

        # Check if article exists in DB (enforcing ingestion first constraint)
        article = await self.article_repository.get(article_id)
        if not article:
            raise ValueError(
                f"Article with ID {article_id} must be ingested before it can be assigned to a Story."
            )

        assoc = await self.repository.assign_article(story_id, article_id, confidence_score)
        if not assoc:
            raise ValueError(f"Failed to assign article {article_id} to story {story_id}.")
        return assoc

    async def remove_article_from_story(self, story_id: int, article_id: int) -> bool:
        story = await self.repository.get(story_id)
        if not story:
            raise ValueError(f"Story with ID {story_id} does not exist.")

        return await self.repository.remove_article(story_id, article_id)
