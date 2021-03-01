# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient

from app.main import app

# https://opensource.zalando.com/restful-api-guidelines/#227
NO_CACHE_HEADERS = "no-cache, no-store, must-revalidate, max-age=0"


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.headers["cache-control"] == NO_CACHE_HEADERS
