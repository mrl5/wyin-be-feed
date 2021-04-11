# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient
from roman import InvalidRomanNumeralError

from feed.errors import UnsupportedLanguageError
from feed.utils.wikidata_api import (
    get_title_id,
    get_wikipedia_title_for_century,
    get_wikipedia_title_for_year,
)
from tests.mocks.fake_wikidata_api import fake_app
from tests.mocks.mock_factory import get_wiki_response

year_titles = [("en", 13, "AD 13"), ("pl", 13, "13")]

century_titles = [("pl", "X", "X wiek"), ("pl", "XIX", "XIX wiek")]
century_exceptions = [
    (1, "pl", InvalidRomanNumeralError),
    ("a", "pl", InvalidRomanNumeralError),
    ("A", "pl", InvalidRomanNumeralError),
    ("x", "pl", InvalidRomanNumeralError),
    ("X1", "pl", InvalidRomanNumeralError),
    ("X", "en", UnsupportedLanguageError),
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


@pytest.mark.parametrize("kwargs, exception", title_id_exceptions)
def test_get_title_id_exceptions(kwargs, exception):
    with pytest.raises(exception):
        get_title_id(get_wiki_response("pl_wikidata_search_entities_century"), **kwargs)
