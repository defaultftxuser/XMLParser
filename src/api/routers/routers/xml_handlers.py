from fastapi import APIRouter, Depends, Query, HTTPException
from httpx import HTTPError
from punq import Container

from src.domain.schemas.response_schema import (
    ResponseOutSchema,
    StatusCodeSchema,
    DescriptionSchema,
    ExtraSchema,
    ResponseSchema,
)
from src.domain.schemas.xml_schemas import XMLSchema
from src.infra.celery.tasks import start_parse_xml_and_save_products
from src.logic.container import init_container
from src.logic.other.http_client import HttpClient
from src.logic.repo_service.mongo_service import MongoService

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/xml")
async def create_summary(
    schema: XMLSchema,
    client: HttpClient = Depends(HttpClient),
) -> ResponseOutSchema:
    try:
        response = await client.make_get_request_and_download(url=schema.url)
        start_parse_xml_and_save_products.apply_async(args=[response])

        return ResponseOutSchema(
            status_code=StatusCodeSchema(status_code=200),
            description=DescriptionSchema(description=""),
            extra=ExtraSchema(
                extra="U can search answer after on date, example='2024-01-01'"
            ),
            text=ResponseSchema(text="Task pending"),
        )

    except HTTPError:
        raise HTTPException(
            status_code=404,
            detail=ResponseOutSchema(
                status_code=StatusCodeSchema(status_code=404),
                description=DescriptionSchema(description=""),
                extra=ExtraSchema(extra=""),
                text=ResponseSchema(text="Wrong url"),
            ),
        )


@router.get("/get_answers")
async def get_answers(
    sale_date: str = Query(default=None, example="2024-01-01"),
    limit: int = Query(default=10),
    offset: int = Query(default=0),
    container: Container = Depends(init_container),
) -> ResponseOutSchema:
    try:
        service: MongoService = container.resolve(MongoService)
        collections = await service.get_answers(
            sale_date=sale_date, offset=offset, limit=limit
        )

        return ResponseOutSchema(
            status_code=StatusCodeSchema(status_code=200),
            description=DescriptionSchema(description=""),
            extra=ExtraSchema(extra=""),
            text=ResponseSchema(text=[collection for collection in collections]),
        )

    except HTTPError:
        raise HTTPException(
            status_code=404,
            detail=ResponseOutSchema(
                status_code=StatusCodeSchema(status_code=404),
                description=DescriptionSchema(description=""),
                extra=ExtraSchema(extra=""),
                text=ResponseSchema(text=""),
            ),
        )
