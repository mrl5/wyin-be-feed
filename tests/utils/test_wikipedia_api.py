# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient

from feed.utils.wikipedia_api import get_wiki_page_content, query_year
from tests.mocks.fake_wikipedia_api import fake_app
from tests.mocks.mock_factory import get_wiki_response

languages = ("pl", "en")
wiki_extracts = [
    (
        get_wiki_response("en_wiki"),
        get_wiki_response("en_wiki")["query"]["pages"]["39974"]["extract"],
    ),
    (
        get_wiki_response("pl_wiki"),
        get_wiki_response("pl_wiki")["query"]["pages"]["13907"]["extract"],
    ),
]


@pytest.fixture(scope="function")
def client():
    o = AsyncClient(app=fake_app)
    return o


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", languages)
async def test_query_year(client, lang):
    client.params.update({"lang": lang})  # this is needed only to parametrize fake_app
    async with client:
        response = await query_year("1000", lang, client)
    assert response == get_wiki_response(f"{lang}_wiki")


@pytest.mark.parametrize("wiki_api_response, wiki_page_content", wiki_extracts)
def test_get_wiki_response(wiki_api_response, wiki_page_content):
    assert get_wiki_page_content(wiki_api_response) == wiki_page_content
