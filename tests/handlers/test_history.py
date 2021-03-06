# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, unique
from typing import Tuple

import pytest
from pydantic import ValidationError

from feed.handlers.history import Events
from feed.interfaces.handlers import IHttpRequestHandler
from tests.mocks.mock_factory import get_events_response

valid_time_params = ({"t": "10:20"}, {"t": "10%3A20"})
invalid_time_params = ({"t": "24:00"}, {"t": "10:60"})


@unique
class HandlersEnum(Enum):
    events = Events


def handler_factory(key, params) -> IHttpRequestHandler:
    a_class = HandlersEnum[key].value
    a_object = a_class(params)
    return a_object


def handlers_factory() -> Tuple[IHttpRequestHandler, ...]:
    return tuple(
        [
            handler_factory(named_value.name, valid_time_params[0])
            for named_value in HandlersEnum
        ]
    )


def test_interface():
    for instance in handlers_factory():
        assert isinstance(instance, IHttpRequestHandler)


@pytest.mark.asyncio
@pytest.mark.parametrize("valid_time_param", valid_time_params)
async def test_events(valid_time_param):
    handler = handler_factory("events", valid_time_param)
    result = await handler.handle()
    assert result.dict() == get_events_response("pl_events")


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_time_param", invalid_time_params)
async def test_events_exceptions(invalid_time_param):
    with pytest.raises(ValidationError):
        handler = handler_factory("events", invalid_time_param)
        await handler.handle()
