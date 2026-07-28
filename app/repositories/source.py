from typing import Optional, Sequence
  from sqlalchemy import select
  from sqlalchemy.ext.asyncio import AsyncSession

  from app.models.source import Source, SourcePolicy
  from app.schemas.source import SourceCreate, SourceUpdate


  class SourceRepository:
      def __init__(self, db: AsyncSession) -> None:
          self.db = db

      async def get(self, source_id: int) -> Optional[Source]:
          result = await self.db.execute(
              select(Source).where(Source.id == source_id)
          )
          return result.scalar_one_or_none()

      async def get_by_url(self, url: str) -> Optional[Source]:
          result = await self.db.execute(
              select(Source).where(Source.url == url)
          )
          return result.scalar_one_or_none()

      async def list(self, skip: int = 0, limit: int = 100) -> Sequence[Source]:
          result = await self.db.execute(
              select(Source).offset(skip).limit(limit)
          )
          return result.scalars().all()

      async def create(self, schema: SourceCreate) -> Source:
          db_source = Source(
              name=schema.name,
              url=str(schema.url),
              description=schema.description,
          )
          self.db.add(db_source)
          await self.db.flush()

          if schema.policy:
              db_policy = SourcePolicy(
                  source_id=db_source.id,
                  crawl_interval_hours=schema.policy.crawl_interval_hours,
                  retry_limit=schema.policy.retry_limit,
                  is_active=schema.policy.is_active,
              )
              self.db.add(db_policy)
              db_source.policy = db_policy

          await self.db.commit()
          await self.db.refresh(db_source)
          return db_source

      async def update(self, source_id: int, schema: SourceUpdate) -> Optional[Source]:
          db_source = await self.get(source_id)
          if not db_source:
              return None

          update_data = schema.model_dump(exclude_unset=True)
          policy_data = update_data.pop("policy", None)

          for field, value in update_data.items():
              if field == "url" and value is not None:
                  setattr(db_source, field, str(value))
              else:
                  setattr(db_source, field, value)

          if policy_data:
              if db_source.policy:
                  for field, value in policy_data.items():
                      setattr(db_source.policy, field, value)
              else:
                  db_policy = SourcePolicy(
                      source_id=db_source.id,
                      crawl_interval_hours=policy_data.get("crawl_interval_hours", 24),
                      retry_limit=policy_data.get("retry_limit", 3),
                      is_active=policy_data.get("is_active", True),
                  )
                  self.db.add(db_policy)
                  db_source.policy = db_policy

          await self.db.commit()
          await self.db.refresh(db_source)
          return db_source

      async def delete(self, source_id: int) -> bool:
          db_source = await self.get(source_id)
          if not db_source:
              return False
          await self.db.delete(db_source)
          await self.db.commit()
          return True
  
