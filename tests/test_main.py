# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from asyncio import wait

import pytest
from httpx import AsyncClient

from feed.conf import ALLOWED_ORIGINS
from feed.main import app
from tests.mocks.mock_factory import get_event_response
from tests.mocks.monkeypatches import (
    monkeypatch_history_event_handler,
    monkeypatch_history_event_random_handler,
)

# https://opensource.zalando.com/restful-api-guidelines/#227
NO_CACHE_HEADERS = "no-cache, no-store, must-revalidate, max-age=0"

history_event_cases = [
    (200, {"t": "9:08"}),
    (200, {"t": "9%3A08"}),
    (200, {"t": "09:08"}),
    (200, {"t": "09:08", "X": "F"}),
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
@pytest.mark.parametrize("status_code, params", history_event_cases)
async def test_history_event(status_code, params, monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/event", params=params)

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json() == get_event_response("pl_event")
    if status_code == 404:
        assert json.loads(response.json())["code"] == "NF001"


@pytest.mark.asyncio
async def test_history_event_random(monkeypatch):
    monkeypatch_history_event_random_handler(monkeypatch)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responses, _ = await wait([ac.get("/history/event/random") for _ in range(10)])

    responses = [r.result() for r in responses]
    assert all(r.status_code == 200 for r in responses) is True
    assert all(r.json() == responses[0].json() for r in responses) is False


@pytest.mark.asyncio
async def test_midnight_response(monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/event", params={"t": "0:00"})
    assert response.status_code == 404
    assert json.loads(response.json())["code"] == "NF002"


@pytest.mark.asyncio
async def test_nocontent_response(monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/history/event", params={"t": "0:57"})
    assert response.status_code == 404
    assert json.loads(response.json())["code"] == "NF003"


@pytest.mark.asyncio
@pytest.mark.parametrize("params", cors_params)
async def test_cors_headers(params, monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    monkeypatch_history_event_random_handler(monkeypatch)
    headers = {"origin": "http://test"}
    responses = []
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responses.append(await ac.get("/history/event", params=params, headers=headers))
        responses.append(await ac.get("/history/event/random", headers=headers))
    for r in responses:
        assert r.headers["access-control-allow-origin"] in ALLOWED_ORIGINS


@pytest.mark.asyncio
async def test_http_timeout(monkeypatch):
    monkeypatch_history_event_handler(monkeypatch, force_timeout=True)
    monkeypatch_history_event_random_handler(monkeypatch, force_timeout=True)
    responses = []
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responses.append(await ac.get("/history/event", params={"t": "10:20"}))
        responses.append(await ac.get("/history/event/random"))
    for r in responses:
        assert r.status_code == 504
