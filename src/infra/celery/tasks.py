import asyncio
from datetime import datetime

from redis import Redis

from src.common.settings.logger import get_logger
from src.infra.celery.client import app
from src.infra.celery.redis import RedisClient
from src.logic.container import init_container
from src.logic.use_case.gpt_usecase import GPTUseCase
from src.logic.use_case.product_category import ParseAndCreateProductCategoryUseCase


logger = get_logger(__name__)


@app.task
def start_parse_xml_and_save_products(
    xml_data: str,
    element: str = "//product",
    parse_and_create_usecase: ParseAndCreateProductCategoryUseCase = init_container().resolve(
        ParseAndCreateProductCategoryUseCase
    ),
    redis_client: Redis = init_container().resolve(RedisClient),
):
    try:

        logger.debug("Starting XML parsing task")
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        logger.debug("Created new event loop")

    asyncio.set_event_loop(loop)

    try:
        _, sale_date = loop.run_until_complete(
            parse_and_create_usecase.parse_and_create(xml_data, element)
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
def gpt_task(
    gpt_usecase: GPTUseCase = init_container().resolve(GPTUseCase),
    redis_client: Redis = init_container().resolve(RedisClient),
):
    try:
        if input_date_bytes := redis_client.get("sale_date"):
            input_date = datetime.strptime(
                input_date_bytes.decode("utf-8"), "%Y-%m-%d"
            ).date()
            logger.debug(f"Starting GPT task with date: {input_date}")
            asyncio.run(
                gpt_usecase.create_summary_by_gpt_and_save(input_date=input_date)
            )
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
