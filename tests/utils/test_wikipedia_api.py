# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient

from feed.utils.wikipedia_api import query
from tests.mocks.fake_wikipedia_api import fake_app
from tests.mocks.mock_factory import get_wiki_response

languages = ("pl", "en")


@pytest.fixture(scope="function")
def client():
    o = AsyncClient(app=fake_app)
    return o


@pytest.mark.asyncio
@pytest.mark.parametrize("lang", languages)
async def test_query(client, lang):
    client.params.update({"lang": lang})  # this is needed only to parametrize fake_app

    response = await query(1000, lang, client)
    assert response.status_code == 200
    assert response.json() == get_wiki_response(f"{lang}_wiki")
