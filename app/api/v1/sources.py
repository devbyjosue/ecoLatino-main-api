from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_source_service
from app.schemas.source import SourceCreate, SourceResponse, SourceUpdate
from app.services.source import SourceService

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("", response_model=SourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    schema: SourceCreate,
    service: SourceService = Depends(get_source_service),
) -> SourceResponse:
    try:
        source = await service.create_source(schema)
        return SourceResponse.model_validate(source)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[SourceResponse])
async def list_sources(
    skip: int = 0,
    limit: int = 100,
    service: SourceService = Depends(get_source_service),
) -> list[SourceResponse]:
    sources = await service.list_sources(skip=skip, limit=limit)
    return [SourceResponse.model_validate(s) for s in sources]


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: int,
    service: SourceService = Depends(get_source_service),
) -> SourceResponse:
    source = await service.get_source(source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
    return SourceResponse.model_validate(source)


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: int,
    schema: SourceUpdate,
    service: SourceService = Depends(get_source_service),
) -> SourceResponse:
    try:
        source = await service.update_source(source_id, schema)
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source with ID {source_id} not found",
            )
        return SourceResponse.model_validate(source)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: int,
    service: SourceService = Depends(get_source_service),
) -> None:
    deleted = await service.delete_source(source_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source with ID {source_id} not found",
        )
