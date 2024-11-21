import asyncio
from dataclasses import dataclass
from datetime import date
import orjson

from src.common.settings.config import ProjectSettings
from src.domain.entities.base_lxml import GPTAnswerEntity
from src.infra.repository.mongo.gpt_answers_repo import GPTAnswersRepo
from src.logic.other.gpt_service import QuerySQLService
from src.logic.other.http_client import HttpClient


@dataclass(eq=False)
class GPTUseCase:
    settings: ProjectSettings
    service: QuerySQLService
    http_client: HttpClient
    repository: GPTAnswersRepo

    async def get_summary(self, input_date: date):
        total_revenue = self.service.get_date_total_revenue(input_date=input_date)
        top_three_products = self.service.get_date_top_three_products(
            input_date=input_date
        )
        top_categories = self.service.get_category_distribution_date(
            input_date=input_date
        )
        return await asyncio.gather(
            total_revenue,
            top_three_products,
            top_categories,
        )

    async def create_summary_by_gpt_and_save(self, input_date: date):
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
        response = await self.http_client.make_post_request(
            url=self.settings.gpt_url,
            json=json_template,
            headers=orjson.loads(self.settings.gpt_headers),
        )
        if response.status_code == 200:
            document = await self.repository.add_one(
                entity=GPTAnswerEntity(
                    date=input_date,
                    answer=response.json()["result"]["alternatives"][0]["message"][
                        "text"
                    ],
                ),
            )
            return document
        return


def update_gpt_template(
    input_date, total_revenue, top_three_products, top_categories, settings
):
    settings = settings
    gpt_text = settings.gpt_text.format(
        input_date, total_revenue, top_three_products, top_categories
    )

    dict_gpt = orjson.loads(settings.gpt_json)
    dict_gpt["messages"][0]["text"] = gpt_text
    return dict_gpt
