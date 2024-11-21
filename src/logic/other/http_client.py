from dataclasses import dataclass

from httpx import AsyncClient


@dataclass(eq=False)
class HttpClient:
    client: AsyncClient

    async def make_post_request(self, url, json, headers):
        async with self.client as client:
            result = await client.post(url=url, json=json, headers=headers, timeout=100)
            return result
