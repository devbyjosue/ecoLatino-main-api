from fastapi import APIRouter

from app.api.v1.analytics import router as analytics_router
from app.api.v1.articles import router as articles_router
from app.api.v1.crawl_jobs import router as crawl_jobs_router
from app.api.v1.health import router as health_router
from app.api.v1.sources import router as sources_router
from app.api.v1.stories import router as stories_router

router = APIRouter()

router.include_router(health_router)
router.include_router(articles_router)
router.include_router(sources_router)
router.include_router(stories_router)
router.include_router(crawl_jobs_router)
router.include_router(analytics_router)
