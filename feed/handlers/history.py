# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import strptime

from pydantic import BaseModel, validator

from feed.handlers.decorators import decode_request_params
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import WikiTextExtractsEnum, WikiUnprocessedModel
from tests.mocks.mock_factory import get_wiki_response


class EventsParams(BaseModel):
    t: str

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        return strptime(v, "%H:%M")


class Events(IHttpRequestHandler):
    @decode_request_params
    def __init__(self, params: dict):
        self._params = EventsParams(**params)

    def _get_type(self) -> str:
        return WikiTextExtractsEnum.wiki_limited_html.value

    async def _get_wiki_response(self) -> dict:
        return get_wiki_response("pl_wiki")

    def _process_raw_resonse(self, raw_response: dict) -> str:
        return raw_response["query"]["pages"]["13907"]["extract"].replace("\n", "")

    async def handle(self) -> WikiUnprocessedModel:
        response = await self._get_wiki_response()
        return WikiUnprocessedModel(
            type=self._get_type(), data=self._process_raw_resonse(response)
        )
