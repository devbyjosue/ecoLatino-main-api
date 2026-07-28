from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Setup logging configuration on startup
    setup_logging()
    logger.info("Starting up FastAPI application...")

    yield

    logger.info("Shutting down FastAPI application...")
