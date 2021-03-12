# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import strptime
from typing import Callable

from pydantic import BaseModel, validator

from feed.handlers.decorators import decode_request_params
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import WikiTextExtractsEnum, WikiUnprocessedModel
from feed.utils.converters import convert_time_to_year
from feed.utils.wikipedia_api import get_wiki_page_content, query_year


class EventsParams(BaseModel):
    t: str

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        strptime(v, "%H:%M")
        return v


class Events(IHttpRequestHandler):
    @decode_request_params
    def __init__(self, params: dict):
        self._params = EventsParams(**params)
        self._lang = "pl"
        self._time_to_year_converter: Callable[[str], int] = convert_time_to_year
        self._data_extractor: Callable[[dict], str] = get_wiki_page_content

    async def handle(self) -> WikiUnprocessedModel:
        response = await self._get_wiki_response()
        data = self._data_extractor(response).replace("\n", "")
        return WikiUnprocessedModel(type=self._get_type(), data=data)

    def _get_type(self) -> str:
        return str(WikiTextExtractsEnum.wiki_limited_html.value)

    async def _get_wiki_response(self) -> dict:
        year = self._time_to_year_converter(self._params.t)
        return await query_year(year, self._lang)
