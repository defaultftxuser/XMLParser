import asyncio
from dataclasses import dataclass
from datetime import date


import orjson

from src.common.settings.config import ProjectSettings
from src.common.settings.logger import get_logger
from src.domain.entities.base_lxml import GPTAnswerEntity

from src.logic.other.gpt_service import QuerySQLService
from src.logic.other.http_client import HttpClient
from src.logic.repo_service.mongo_service import MongoService

logger = get_logger(__name__)


@dataclass(eq=False)
class GPTUseCase:
    settings: ProjectSettings
    service: QuerySQLService
    http_client: HttpClient
    mongo_service: MongoService

    async def get_summary(self, input_date: date):
        try:
            logger.info(f"Fetching summary for date: {input_date}")
            total_revenue = self.service.get_date_total_revenue(input_date=input_date)
            top_three_products = self.service.get_date_top_three_products(
                input_date=input_date
            )
            top_categories = self.service.get_category_distribution_date(
                input_date=input_date
            )
            result = await asyncio.gather(
                total_revenue,
                top_three_products,
                top_categories,
            )
            logger.info(f"Summary fetched successfully for date: {input_date}")
            return result
        except Exception as e:
            logger.error(f"Error fetching summary for date {input_date}: {e}")
            raise

    async def create_summary_by_gpt_and_save(self, input_date: date):
        try:
            logger.info(f"Starting GPT summary creation for date: {input_date}")
            total_revenue, top_three_products, top_categories = await self.get_summary(
                input_date=input_date
            )

            json_template = update_gpt_template(
                input_date=input_date,
                total_revenue=total_revenue,
                top_three_products=", ".join(map(str, top_three_products)),
                top_categories=top_categories,
                settings=self.settings,
            )

            logger.debug(f"Generated GPT request template: {json_template}")
            headers = get_headers_for_gpt(self.settings.iam_token)
            response = await self.http_client.make_post_request(
                url=self.settings.gpt_url,
                json=json_template,
                headers=headers,
            )

            if response.status_code == 401:
                response = await self.http_client.make_post_request(
                    url=self.settings.iam_token_url,
                    json=self.settings.yandex_oauth_json,
                )
            token = response.json().get("iamToken", None)
            headers = get_headers_for_gpt(token)
            response = await self.http_client.make_post_request(
                url=self.settings.gpt_url,
                json=json_template,
                headers=headers,
            )

            logger.info(f"GPT request successful for date: {input_date}")
            try:
                document = await self.mongo_service.add_one(
                    entity=GPTAnswerEntity(
                        sale_date=input_date,
                        answer=response.json()["result"]["alternatives"][0]["message"][
                            "text"
                        ],
                    )
                )
                logger.info(f"Summary saved to database for date: {input_date}")
                return document
            except Exception as e:
                logger.error(
                    f"Error saving GPT answer to database for date {input_date}: {e}"
                )
        except Exception as e:
            logger.error(
                f"Error during GPT summary creation for date {input_date}: {e}"
            )
            raise


def update_gpt_template(
    input_date, total_revenue, top_three_products, top_categories, settings
):
    try:
        gpt_text = settings.gpt_text.format(
            input_date, total_revenue, top_three_products, top_categories
        )
        dict_gpt = orjson.loads(settings.gpt_json)
        dict_gpt["messages"][0]["text"] = gpt_text
        logger.debug(f"Updated GPT template for date: {input_date}")
        return dict_gpt
    except Exception as e:
        logger.error(f"Error updating GPT template for date {input_date}: {e}")
        raise


def get_headers_for_gpt(token: str) -> dict:
    return {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
