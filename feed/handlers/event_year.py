# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import validator

from feed.handlers._event import _Event, _EventParams
from feed.handlers.decorators import decode_request_params
from feed.models.history import SingleHistoryEventModel
from feed.utils.converters import throw_on_invalid_year


class EventYearParams(_EventParams):
    year: int

    @validator("year")
    def valid_year(cls, v):
        y = int(v)
        throw_on_invalid_year(y)
        return y


class EventYear(_Event):
    @decode_request_params
    def __init__(self, params: dict):
        super().__init__(params)
        self._params: EventYearParams = EventYearParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = self._params.year
        return await super().handle()
