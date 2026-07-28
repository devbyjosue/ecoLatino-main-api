from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimeStampedModel
from app.models.enums import CrawlJobStatus

if TYPE_CHECKING:
    from app.models.source import Source


class CrawlJob(Base, TimeStampedModel):
    __tablename__ = "crawl_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[CrawlJobStatus] = mapped_column(
        Enum(CrawlJobStatus),
        default=CrawlJobStatus.PENDING,
        nullable=False,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    items_crawled: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    source: Mapped["Source"] = relationship("Source", back_populates="crawl_jobs")
