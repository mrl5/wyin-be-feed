# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import strptime

from pydantic import validator

from feed.handlers._event import _Event, _EventParams
from feed.handlers.decorators import decode_request_params
from feed.models.history import SingleHistoryEventModel
from feed.utils.converters import convert_time_to_year


class EventTimeParams(_EventParams):
    t: str

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        strptime(v, "%H:%M")
        return v


class EventTime(_Event):
    @decode_request_params
    def __init__(self, params: dict):
        super().__init__(params)
        self._params: EventTimeParams = EventTimeParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = convert_time_to_year(self._params.t)
        return await super().handle()
