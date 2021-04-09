# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import URL, AsyncClient, Response

from feed.utils.http_factory import get_async_client
from feed.utils.wikidata_api import (
    get_wikipedia_title_for_century,
    get_wikipedia_title_for_year,
)


async def query_year(year: int, lang: str, client: AsyncClient = None) -> dict:
    client = client if client is not None else get_async_client()
    title = await get_wikipedia_title_for_year(year, lang, client)
    response = await query(title, lang, client)
    return response.json()


async def query_century(century: str, lang: str, client: AsyncClient = None) -> dict:
    client = client if client is not None else get_async_client()
    title = await get_wikipedia_title_for_century(century, lang, client)
    response = await query(title, lang, client)
    return response.json()


async def query(title: str, lang: str, client: AsyncClient) -> Response:
    client.base_url = URL(f"https://{lang}.wikipedia.org")
    client.params.update({"action": "query", "prop": "extracts", "format": "json"})
    async with client:
        return await client.get("/w/api.php", params={"titles": title})


def get_wiki_page_content(json_response: dict) -> str:
    pages = json_response["query"]["pages"]
    page = next(iter(pages))
    return pages[page]["extract"]
