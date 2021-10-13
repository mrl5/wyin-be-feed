# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime
from random import randrange

from feed.handlers.decorators import decode_request_params
from feed.handlers.event import Event, EventParams
from feed.models.history import SingleHistoryEventModel


class EventRandomParams(EventParams):
    pass


class EventRandom(Event):
    @decode_request_params
    def __init__(self, params: dict = {}):
        super().__init__(params)
        self._params: EventRandomParams = EventRandomParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = self._get_random_year()
        return await super().handle()

    def _get_random_year(self) -> int:
        return randrange(1, datetime.now().year)
