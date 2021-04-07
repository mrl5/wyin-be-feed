# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import URL, AsyncClient, Response

from feed.utils.http_factory import get_async_client


async def get_wikipedia_title_for_year(
    year: int, lang: str, client: AsyncClient = None
) -> str:
    client = client if client is not None else get_async_client()
    entities = await search_entities(str(year), lang, client)
    title_id = get_title_id(entities, "year")
    entities = await get_entities(title_id, lang, client)
    return get_title(entities, title_id, lang)


async def search_entities(keyword: str, lang: str, client: AsyncClient) -> dict:
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": lang,
        "search": keyword,
    }
    response = await query(client, **params)
    return response.json()


async def get_entities(title_id: str, lang: str, client: AsyncClient) -> dict:
    client.params.update({"language": lang})
    params = {
        "action": "wbgetentities",
        "format": "json",
        "props": "sitelinks",
        "sitefilter": f"{lang}wiki",
        "ids": title_id,
    }
    response = await query(client, **params)
    return response.json()


async def query(client: AsyncClient, **kwargs) -> Response:
    client.base_url = URL("https://www.wikidata.org")
    async with client:
        return await client.get("/w/api.php", params=kwargs)


def get_title_id(entities: dict, description: str) -> str:
    item = next(
        item for item in entities["search"] if item["description"] == description
    )
    return item["id"]


def get_title(entities: dict, title_id: str, lang: str):
    return entities["entities"][title_id]["sitelinks"][f"{lang}wiki"]["title"]
