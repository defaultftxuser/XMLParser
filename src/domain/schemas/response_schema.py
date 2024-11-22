from typing import Any

from pydantic import BaseModel


class StatusCodeSchema(BaseModel):
    status_code: int


class DescriptionSchema(BaseModel):
    description: str


class ExtraSchema(BaseModel):
    extra: Any


class ResponseSchema(BaseModel):
    text: Any


class ResponseOutSchema(BaseModel):
    status_code: StatusCodeSchema
    description: DescriptionSchema
    extra: ExtraSchema
    text: ResponseSchema
