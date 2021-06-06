# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

from asyncio import gather

from httpx import AsyncClient, Response
from roman import InvalidRomanNumeralError, fromRoman

from feed.conf import SUPPORTED_LANGUAGES
from feed.errors import UnsupportedLanguageError
from feed.utils.converters import convert_year_to_century
from feed.utils.http_factory import get_async_client


class CenturyAndYearTitles(TypedDict):
    century_title: str
    year_title: str


async def get_wikipedia_titles_for_century_and_year(
    year: int, lang: str, client: AsyncClient = None
) -> CenturyAndYearTitles:
    client = client if client is not None else get_async_client()
    century = convert_year_to_century(year)

    century_entities, year_entities = await gather(
        search_entities(get_century_keyword(century), lang, client),
        search_entities(str(year), lang, client),
    )

    century_title_id = get_century_title_id(century_entities)
    year_title_id = get_year_title_id(year_entities)
    ids = "|".join([century_title_id, year_title_id])
    entities = await get_entities(ids, lang, client)

    return {
        "century_title": get_title(entities, century_title_id, lang),
        "year_title": get_title(entities, year_title_id, lang),
    }


async def get_wikipedia_title_for_year(
    year: int, lang: str, client: AsyncClient = None
) -> str:
    client = client if client is not None else get_async_client()
    entities = await search_entities(str(year), lang, client)
    title_id = get_year_title_id(entities)
    entities = await get_entities(title_id, lang, client)
    return get_title(entities, title_id, lang)


async def get_wikipedia_title_for_century(
    century: str, lang: str, client: AsyncClient = None
) -> str:
    client = client if client is not None else get_async_client()
    keyword = get_century_keyword(century)
    entities = await search_entities(keyword, lang, client)
    title_id = get_century_title_id(entities)
    entities = await get_entities(title_id, lang, client)
    return get_title(entities, title_id, lang)


async def search_entities(keyword: str, lang: str, client: AsyncClient) -> dict:
    throw_on_unsupported_language(lang)
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": lang,
        "search": keyword,
    }
    response = await query(client, **params)
    return response.json()


async def get_entities(title_id: str, lang: str, client: AsyncClient) -> dict:
    throw_on_unsupported_language(lang)
    sitefilter = get_sitefilter(lang)
    params = {
        "action": "wbgetentities",
        "format": "json",
        "props": "sitelinks",
        "sitefilter": sitefilter,
        "ids": title_id,
        "language": lang,
    }
    response = await query(client, **params)
    return response.json()


async def query(client: AsyncClient, **kwargs) -> Response:
    return await client.get("https://www.wikidata.org/w/api.php", params=kwargs)


def get_century_keyword(century: str) -> str:
    throw_on_bad_roman_number(century)
    return f"{century} wiek"


def get_century_title_id(entities: dict) -> str:
    return get_title_id(entities, label="century")


def get_year_title_id(entities: dict) -> str:
    pattern = re.compile(r"^year[.,]?$|^year[ .,].+$|.+[ ]year[ .,].*|[ ]year$")
    return get_title_id(entities, description=pattern)


def get_title_id(
    entities: dict, description: re.Pattern = None, label: str = None
) -> str:
    if (description is None and label is None) or (
        description is not None and label is not None
    ):
        raise ValueError("either description or label must be specified")
    if description is not None:
        item = next(
            item
            for item in entities["search"]
            if description.search(item["description"])
        )
    if label is not None:
        item = next(
            item for item in entities["search"] if item["label"].endswith(label)
        )
    return item["id"]


def get_title(entities: dict, title_id: str, lang: str) -> str:
    sitefilter = get_sitefilter(lang)
    return entities["entities"][title_id]["sitelinks"][sitefilter]["title"]


def get_sitefilter(lang: str) -> str:
    return f"{lang.replace('-', '_')}wiki"


def throw_on_bad_roman_number(roman_number: str) -> None:
    if not isinstance(roman_number, str):
        raise InvalidRomanNumeralError(roman_number)
    fromRoman(roman_number)


def throw_on_unsupported_language(
    language: str, supported_languages: list = SUPPORTED_LANGUAGES
) -> None:
    if language not in supported_languages:
        raise UnsupportedLanguageError(f"unsupported language: {language}")
