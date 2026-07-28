from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_crawl_job_service
from app.schemas.crawl_job import CrawlJobCreate, CrawlJobResponse, CrawlJobUpdate
from app.services.crawl_job import CrawlJobService

router = APIRouter(prefix="/crawl-jobs", tags=["crawl-jobs"])


@router.post("", response_model=CrawlJobResponse, status_code=status.HTTP_201_CREATED)
async def create_crawl_job(
    schema: CrawlJobCreate,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> CrawlJobResponse:
    try:
        job = await service.create_job(schema)
        return CrawlJobResponse.model_validate(job)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[CrawlJobResponse])
async def list_crawl_jobs(
    skip: int = 0,
    limit: int = 100,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> list[CrawlJobResponse]:
    jobs = await service.list_jobs(skip=skip, limit=limit)
    return [CrawlJobResponse.model_validate(j) for j in jobs]


@router.get("/source/{source_id}", response_model=list[CrawlJobResponse])
async def list_crawl_jobs_by_source(
    source_id: int,
    skip: int = 0,
    limit: int = 100,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> list[CrawlJobResponse]:
    try:
        jobs = await service.list_jobs_by_source(source_id, skip=skip, limit=limit)
        return [CrawlJobResponse.model_validate(j) for j in jobs]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{job_id}", response_model=CrawlJobResponse)
async def get_crawl_job(
    job_id: int,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> CrawlJobResponse:
    job = await service.get_job(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrawlJob with ID {job_id} not found",
        )
    return CrawlJobResponse.model_validate(job)


@router.put("/{job_id}", response_model=CrawlJobResponse)
async def update_crawl_job(
    job_id: int,
    schema: CrawlJobUpdate,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> CrawlJobResponse:
    job = await service.update_job(job_id, schema)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrawlJob with ID {job_id} not found",
        )
    return CrawlJobResponse.model_validate(job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crawl_job(
    job_id: int,
    service: CrawlJobService = Depends(get_crawl_job_service),
) -> None:
    deleted = await service.delete_job(job_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CrawlJob with ID {job_id} not found",
        )
