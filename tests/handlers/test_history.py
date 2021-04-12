# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, unique

import pytest
from pydantic import ValidationError

from feed.handlers.history import Event, Events
from feed.interfaces.handlers import IHttpRequestHandler
from tests.mocks.mock_factory import (
    get_event_response,
    get_events_response,
    get_wiki_response,
    monkeypatch_history_event_handler,
    monkeypatch_history_events_handler,
)


@unique
class HandlersEnum(Enum):
    event = Event
    events = Events


def handler_factory(key, params) -> IHttpRequestHandler:
    a_class = HandlersEnum[key].value
    a_object = a_class(params)
    return a_object


valid_time_params = ({"t": "9:08"}, {"t": "09%3A08"})
invalid_time_params = ({"t": "24:00"}, {"t": "10:60"})

handlers = tuple(
    [
        handler_factory(named_value.name, valid_time_params[0])
        for named_value in HandlersEnum
    ]
)

fallback_cases = [
    (
        handler_factory("event", {"t": "9:12"}),
        get_wiki_response("pl_wiki_year_912")["query"]["pages"]["13551"]["extract"],
    )
]


@pytest.fixture(scope="function")
def event_handler(monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    o = handler_factory("event", valid_time_params[0])
    return o


@pytest.fixture(scope="function")
def event_handler_912(monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    o = handler_factory("event", {"t": "9:12"})
    return o


@pytest.fixture(scope="function")
def events_handler(monkeypatch):
    monkeypatch_history_events_handler(monkeypatch)
    o = handler_factory("events", valid_time_params[0])
    return o


@pytest.mark.parametrize("handler", handlers)
def test_interface(handler):
    assert isinstance(handler, IHttpRequestHandler)


@pytest.mark.asyncio
@pytest.mark.parametrize("valid_time_param", valid_time_params)
async def test_event(valid_time_param, event_handler):
    result = await event_handler.handle()
    assert result.dict() == get_event_response("pl_event")


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_time_param", invalid_time_params)
async def test_event_exceptions(invalid_time_param):
    with pytest.raises(ValidationError):
        handler = handler_factory("event", invalid_time_param)
        await handler.handle()


@pytest.mark.asyncio
@pytest.mark.parametrize("handler, source", fallback_cases)
async def test_event_fallback(handler, source, monkeypatch):
    monkeypatch_history_event_handler(monkeypatch)
    result = await handler.handle()
    assert result.dict()["data"] is not None
    assert source.find(result.dict()["data"]) > 0


@pytest.mark.asyncio
@pytest.mark.parametrize("valid_time_param", valid_time_params)
async def test_events(valid_time_param, events_handler):
    result = await events_handler.handle()
    assert result.dict() == get_events_response("pl_events")


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_time_param", invalid_time_params)
async def test_events_exceptions(invalid_time_param):
    with pytest.raises(ValidationError):
        handler = handler_factory("events", invalid_time_param)
        await handler.handle()
