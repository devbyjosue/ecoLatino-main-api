import asyncio
import sys
from app.core.database import engine
from app.models.base import Base

# Importar todos los modelos para que SQLAlchemy los registre en Base.metadata
from app.models.source import Source, SourcePolicy
from app.models.article import Article
from app.models.story import Story, StoryArticle
from app.models.crawl_job import CrawlJob

async def create_tables():
    print("Conectándose a la base de datos Neon y creando tablas...")
    try:
        async with engine.begin() as conn:
            # Crear todas las tablas que no existan
            await conn.run_sync(Base.metadata.create_all)
        print("¡Tablas creadas exitosamente en tu base de datos Neon!")
    except Exception as e:
        print(f"Error al crear las tablas: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(create_tables())
