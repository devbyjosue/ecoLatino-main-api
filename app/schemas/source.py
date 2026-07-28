from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


# SourcePolicy Schemas
class SourcePolicyBase(BaseModel):
    crawl_interval_hours: int = Field(default=24, ge=1)
    retry_limit: int = Field(default=3, ge=0)
    is_active: bool = True


class SourcePolicyCreate(SourcePolicyBase):
    pass


class SourcePolicyUpdate(BaseModel):
    crawl_interval_hours: Optional[int] = Field(default=None, ge=1)
    retry_limit: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class SourcePolicyResponse(SourcePolicyBase):
    id: int
    source_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Source Schemas
class SourceBase(BaseModel):
    name: str = Field(..., max_length=255)
    url: HttpUrl
    description: Optional[str] = Field(None, max_length=1000)


class SourceCreate(SourceBase):
    policy: Optional[SourcePolicyCreate] = None


class SourceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    url: Optional[HttpUrl] = None
    description: Optional[str] = Field(None, max_length=1000)
    policy: Optional[SourcePolicyUpdate] = None


class SourceResponse(SourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    policy: Optional[SourcePolicyResponse] = None

    model_config = ConfigDict(from_attributes=True)
