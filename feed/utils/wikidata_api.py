# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import URL, AsyncClient, Response
from roman import InvalidRomanNumeralError, fromRoman

from feed.errors import UnsupportedLanguageError
from feed.utils.http_factory import get_async_client


async def get_wikipedia_title_for_year(
    year: int, lang: str, client: AsyncClient = None
) -> str:
    client = client if client is not None else get_async_client()
    entities = await search_entities(str(year), lang, client)
    title_id = get_title_id(entities, description="year")
    entities = await get_entities(title_id, lang, client)
    return get_title(entities, title_id, lang)


async def get_wikipedia_title_for_century(
    century: str, lang: str, client: AsyncClient = None
) -> str:
    supported_languages = ["pl"]
    throw_on_unsupported_language(lang, supported_languages)
    throw_on_bad_roman_number(century)

    client = client if client is not None else get_async_client()
    keyword = f"{century} wiek"
    entities = await search_entities(keyword, lang, client)
    title_id = get_title_id(entities, label="century")
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


def get_title_id(entities: dict, description: str = None, label: str = None) -> str:
    if (description is None and label is None) or (
        description is not None and label is not None
    ):
        raise ValueError("either description or label must be specified")
    if description is not None:
        item = next(
            item for item in entities["search"] if item["description"] == description
        )
    if label is not None:
        item = next(
            item for item in entities["search"] if item["label"].endswith(label)
        )
    return item["id"]


def get_title(entities: dict, title_id: str, lang: str) -> str:
    return entities["entities"][title_id]["sitelinks"][f"{lang}wiki"]["title"]


def throw_on_bad_roman_number(roman_number: str) -> None:
    if not isinstance(roman_number, str):
        raise InvalidRomanNumeralError(roman_number)
    fromRoman(roman_number)


def throw_on_unsupported_language(language: str, supported_languages: list) -> None:
    if language not in supported_languages:
        raise UnsupportedLanguageError(f"unsupported language: {language}")
