# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import URL, AsyncClient

from feed.utils.http_factory import get_async_client


async def query_year(year: int, lang: str, client: AsyncClient = None) -> dict:
    client = client if client is not None else get_async_client()

    client.base_url = URL(f"https://{lang}.wikipedia.org")
    client.params.update({"action": "query", "prop": "extracts", "format": "json"})

    async with client:
        response = await client.get("/w/api.php", params={"titles": year})
    return response.json()


def get_wiki_page_content(json_response: dict) -> str:
    pages = json_response["query"]["pages"]
    page = next(iter(pages))
    return pages[page]["extract"]
