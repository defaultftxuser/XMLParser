import asyncio
from src.infra.celery.client import app
from src.logic.use_case.product_category import (
    get_parse_and_create_products,
)


@app.task
def start_parse_xml_and_save_products(xml_data: str, element: str = "//product"):
    asyncio.run(get_parse_and_create_products().parse_and_create(xml_data, element))


@app.task
def gpt_task():
    ...

