from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimeStampedModel

if TYPE_CHECKING:
    from app.models.article import Article
    from app.models.crawl_job import CrawlJob


class Source(Base, TimeStampedModel):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Relationships
    # Source has zero or one SourcePolicy
    policy: Mapped[Optional["SourcePolicy"]] = relationship(
        "SourcePolicy",
        back_populates="source",
        uselist=False,
        cascade="all, delete-orphan",
    )
    # Source has many Articles
    articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="source",
        cascade="all, delete-orphan",
    )
    # Source has many CrawlJobs
    crawl_jobs: Mapped[list["CrawlJob"]] = relationship(
        "CrawlJob",
        back_populates="source",
        cascade="all, delete-orphan",
    )


class SourcePolicy(Base, TimeStampedModel):
    __tablename__ = "source_policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    crawl_interval_hours: Mapped[int] = mapped_column(Integer, default=24, nullable=False)
    retry_limit: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    source: Mapped["Source"] = relationship("Source", back_populates="policy")
