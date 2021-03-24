# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from httpx import AsyncClient

from feed.main import allowed_origins, app
from tests.mocks.mock_factory import (
    get_events_response,
    monkeypatch_history_events_handler,
)

# https://opensource.zalando.com/restful-api-guidelines/#227
NO_CACHE_HEADERS = "no-cache, no-store, must-revalidate, max-age=0"

history_events_cases = [
    (200, {"t": "10:20"}),
    (200, {"t": "10%3A20"}),
    (200, {"t": "8:10"}),
    (200, {"t": "10:20", "X": "F"}),
    (400, {"t": "1:1"}),
    (400, {"t": "hh:mm"}),
    (400, {"t": ""}),
    (400, {"t": "24:21"}),
    (400, {"t": "20:60"}),
    (400, {"t": "8:10PM"}),
    (400, {"ty": "10:20"}),
    (400, {"T": "10:20"}),
    (400, {}),
    (400, None),
    (400, {"t": "-8:23"}),
    (404, {"t": "23:59"}),
]

cors_params = ({"t": "10:20"}, {"t": "23:59"})


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.headers["cache-control"] == NO_CACHE_HEADERS


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code, params", history_events_cases)
async def test_history_events(status_code, params, monkeypatch):
    monkeypatch_history_events_handler(monkeypatch)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/events", params=params)

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json() == get_events_response("pl_events")


@pytest.mark.asyncio
@pytest.mark.parametrize("params", cors_params)
async def test_cors_headers(params, monkeypatch):
    monkeypatch_history_events_handler(monkeypatch)
    headers = {"origin": "http://test"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/events", params=params, headers=headers)
    assert response.headers["access-control-allow-origin"] in allowed_origins


@pytest.mark.asyncio
async def test_http_timeout(monkeypatch):
    monkeypatch_history_events_handler(monkeypatch, force_timeout=True)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/events", params={"t": "10:20"})
    assert response.status_code == 504
