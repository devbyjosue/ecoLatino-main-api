from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimeStampedModel

if TYPE_CHECKING:
    from app.models.source import Source
    from app.models.story import StoryArticle


class Article(Base, TimeStampedModel):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    source: Mapped["Source"] = relationship("Source", back_populates="articles")

    # Many-to-many relationship through StoryArticle association object
    story_associations: Mapped[list["StoryArticle"]] = relationship(
        "StoryArticle",
        back_populates="article",
        cascade="all, delete-orphan",
    )
