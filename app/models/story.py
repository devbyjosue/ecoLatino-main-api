from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimeStampedModel

if TYPE_CHECKING:
    from app.models.article import Article


class Story(Base, TimeStampedModel):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    # Story has many Articles through StoryArticle
    article_associations: Mapped[list["StoryArticle"]] = relationship(
        "StoryArticle",
        back_populates="story",
        cascade="all, delete-orphan",
    )


class StoryArticle(Base):
    __tablename__ = "story_articles"

    story_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("stories.id", ondelete="CASCADE"),
        primary_key=True,
    )
    article_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("articles.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Relationship metadata
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    story: Mapped["Story"] = relationship("Story", back_populates="article_associations")
    article: Mapped["Article"] = relationship("Article", back_populates="story_associations")
