import asyncio
from datetime import datetime

from redis import Redis

from src.common.settings.logger import get_logger
from src.infra.celery.client import app
from src.logic.use_case.gpt_usecase import get_gpt_usecase
from src.logic.use_case.product_category import (
    get_parse_and_create_products,
)

redis_client = Redis()
logger = get_logger(__name__)


@app.task
def start_parse_xml_and_save_products(xml_data: str, element: str = "//product"):
    try:
        logger.debug("Starting XML parsing task")
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        logger.debug("Created new event loop")

    asyncio.set_event_loop(loop)

    try:
        _, sale_date = loop.run_until_complete(
            get_parse_and_create_products().parse_and_create(xml_data, element)
        )
        redis_client.set("sale_date", str(sale_date))
        logger.info(
            f"Successfully parsed and created products, cached sale date: {sale_date}"
        )
        return f"Successfully created objects, cached key {str(sale_date)}"
    except Exception as e:
        logger.error(f"Error occurred while parsing XML and creating products: {e}")
        raise e


@app.task
def gpt_task():
    usecase = get_gpt_usecase()
    try:
        if input_date_bytes := redis_client.get("sale_date"):
            input_date = datetime.strptime(
                input_date_bytes.decode("utf-8"), "%Y-%m-%d"
            ).date()
            logger.debug(f"Starting GPT task with date: {input_date}")
            asyncio.run(usecase.create_summary_by_gpt_and_save(input_date=input_date))
            logger.info(f"Task with {input_date} started")
            return f"Task with {input_date} started"
        else:
            logger.warning("No 'sale_date' found in Redis")
            return "No sale date found"
    except Exception as e:
        logger.error(f"Error occurred while executing GPT task: {e}")
        raise e

    finally:
        redis_client.delete("sale_date")
