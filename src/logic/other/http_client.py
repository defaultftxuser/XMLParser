from dataclasses import dataclass
from http import HTTPStatus
from typing import Any
from httpx._exceptions import HTTPError  # noqa

from httpx import AsyncClient, RequestError

from src.common.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(eq=False)
class HttpClient:
    client = AsyncClient

    async def make_post_request(
        self,
        url,
        json: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ):
        logger.debug(
            f"Sending POST request. URL: {url}, Headers: {headers}, Body: {json}"
        )

        try:
            async with self.client() as client:
                result = await client.post(
                    url=url, json=json, headers=headers, timeout=100
                )

                if result.status_code == HTTPStatus.OK:
                    logger.info(
                        f"POST request successful. URL: {url}, Status Code: {result.status_code}, Response: {result.json()}"
                    )
                else:
                    logger.warning(
                        f"POST request failed. URL: {url}, Status Code: {result.status_code}, Response: {result.text[:50]}..."
                    )

                return result

        except RequestError as e:
            logger.error(
                f"Request error occurred while sending POST request to {url}. Error: {e}"
            )
            raise e
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while sending POST request to {url}. Error: {e}"
            )
            raise e

    async def make_get_request_and_download(
        self, url: str, headers: dict[str, Any] | None = None
    ) -> str:
        response = await self.client().get(url=url, headers=headers)
        if response.status_code >= 400:
            logger.exception(f"can't get request by {url=}, {response.status_code=}")
            raise HTTPError

        return response.text


def get_http_client() -> HttpClient:
    return HttpClient()
