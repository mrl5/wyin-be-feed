# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient
from roman import InvalidRomanNumeralError

from feed.errors import UnsupportedLanguageError
from feed.utils.wikidata_api import (
    CenturyAndYearTitles,
    get_title_id,
    get_wikipedia_title_for_century,
    get_wikipedia_title_for_year,
    get_wikipedia_titles_for_century_and_year,
    get_year_title_id,
)
from tests.mocks.fake_wikidata_api import fake_app
from tests.mocks.mock_factory import get_wiki_response

year_titles = [("en", 13, "AD 13"), ("pl", 13, "13")]
year_title_ids = [
    ({"search": [{"id": "Q23411", "description": "year"}]}, "Q23411"),
    ({"search": [{"id": "Q49628", "description": "current year"}]}, "Q49628"),
    (
        {"search": [{"id": "Q24783", "description": "year in the Julian Calendar"}]},
        "Q24783",
    ),
    (
        {"search": [{"id": "Q2035", "description": "common year starting on Tuesday"}]},
        "Q2035",
    ),
    (
        {"search": [{"id": "Q2056", "description": "leap year starting on Wednesday"}]},
        "Q2056",
    ),
    ({"search": [{"id": "regextest", "description": "year"}]}, "regextest"),
    ({"search": [{"id": "regextest", "description": "a year."}]}, "regextest"),
    ({"search": [{"id": "regextest", "description": "year."}]}, "regextest"),
    ({"search": [{"id": "regextest", "description": "foo, year"}]}, "regextest"),
    ({"search": [{"id": "regextest", "description": "year, bar"}]}, "regextest"),
    ({"search": [{"id": "regextest", "description": "bar year foo"}]}, "regextest"),
]
year_title_id_exceptions = (
    {"search": [{"id": "regextest", "description": "ayear"}]},
    {"search": [{"id": "regextest", "description": "yeara"}]},
)

century_titles = [("pl", "X", "X wiek"), ("pl", "XIX", "XIX wiek")]
century_exceptions = [
    (1, "pl", InvalidRomanNumeralError),
    ("a", "pl", InvalidRomanNumeralError),
    ("A", "pl", InvalidRomanNumeralError),
    ("x", "pl", InvalidRomanNumeralError),
    ("X1", "pl", InvalidRomanNumeralError),
    ("X", "foobar", UnsupportedLanguageError),
]

century_year_cases = [
    ("pl", 912, CenturyAndYearTitles(century_title="X wiek", year_title="912"))
]

title_id_exceptions = [
    ({"description": None, "label": None}, ValueError),
    ({"description": "century", "label": "century"}, ValueError),
]


@pytest.fixture(scope="function")
def client():
    o = AsyncClient(app=fake_app)
    return o


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, year, title", year_titles)
async def test_get_wikipedia_title_for_year(lang, year, title, client):
    async with client:
        response = await get_wikipedia_title_for_year(year, lang, client)
    assert response == title


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, century, title", century_titles)
async def test_get_wikipedia_title_for_century(lang, century, title, client):
    async with client:
        response = await get_wikipedia_title_for_century(century, lang, client)
    assert response == title


@pytest.mark.asyncio
@pytest.mark.parametrize("century, lang, exception", century_exceptions)
async def test_get_wikipedia_title_for_century_exceptions(century, lang, exception):
    with pytest.raises(exception):
        await get_wikipedia_title_for_century(century, lang)


@pytest.mark.asyncio
@pytest.mark.parametrize("lang, year, response", century_year_cases)
async def test_get_wikipedia_titles_for_century_and_year(lang, year, response, client):
    async with client:
        result = await get_wikipedia_titles_for_century_and_year(year, lang, client)
    assert result == response


@pytest.mark.parametrize("entities, title_id", year_title_ids)
def test_get_year_title_id(entities, title_id):
    assert get_year_title_id(entities) == title_id


@pytest.mark.parametrize("entities", year_title_id_exceptions)
def test_get_year_title_id_exceptions(entities):
    with pytest.raises(Exception):
        get_year_title_id(entities)


@pytest.mark.parametrize("kwargs, exception", title_id_exceptions)
def test_get_title_id_exceptions(kwargs, exception):
    with pytest.raises(exception):
        get_title_id(get_wiki_response("pl_wikidata_search_entities_century"), **kwargs)
