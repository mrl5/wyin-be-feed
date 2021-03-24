# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient

from feed.utils.wikidata_api import get_wikipedia_title_for_year
from tests.mocks.fake_wikidata_api import fake_app

year_titles = [("en", 13, "AD 13"), ("pl", 13, "13")]


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
