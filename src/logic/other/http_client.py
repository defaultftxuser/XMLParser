from dataclasses import dataclass
from http import HTTPStatus

from httpx import AsyncClient, RequestError

from src.common.settings.logger import get_logger

logger = get_logger(__name__)


@dataclass(eq=False)
class HttpClient:
    client: AsyncClient

    async def make_post_request(self, url, json, headers):
        logger.debug(
            f"Sending POST request. URL: {url}, Headers: {headers}, Body: {json}"
        )

        try:
            async with self.client as client:
                result = await client.post(
                    url=url, json=json, headers=headers, timeout=100
                )

                if result.status_code == HTTPStatus.OK:
                    logger.info(
                        f"POST request successful. URL: {url}, Status Code: {result.status_code}, Response: {result.json()}"
                    )
                else:
                    logger.warning(
                        f"POST request failed. URL: {url}, Status Code: {result.status_code}, Response: {result.text}"
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
