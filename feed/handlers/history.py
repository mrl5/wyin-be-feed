# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import strptime
from typing import Callable, Optional

from pydantic import BaseModel, validator

from feed.handlers.decorators import decode_request_params
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import (
    SingleHistoryEventModel,
    WikiTextExtractsEnum,
    WikiUnprocessedModel,
)
from feed.utils.converters import convert_time_to_year, convert_year_to_century
from feed.utils.scrapers import get_year_event_from_century_page
from feed.utils.wikipedia_api import get_wiki_page_content, query_century, query_year


class EventParams(BaseModel):
    t: str

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        strptime(v, "%H:%M")
        return v


class EventsParams(EventParams):
    ...


class Event(IHttpRequestHandler):
    @decode_request_params
    def __init__(self, params: dict):
        self._params = EventParams(**params)
        self._year: int
        self._lang = "pl"
        self._time_to_year_converter: Callable[[str], int] = convert_time_to_year
        self._year_to_century_converter: Callable[[int], str] = convert_year_to_century
        self._html_extractor: Callable[[dict], str] = get_wiki_page_content
        self._data_extractor: Callable[
            [int, str], Optional[str]
        ] = get_year_event_from_century_page

    async def handle(self) -> SingleHistoryEventModel:
        self._year = self._time_to_year_converter(self._params.t)
        response = await self._get_wiki_response()
        html = self._html_extractor(response)
        data = self._data_extractor(self._year, html)
        return SingleHistoryEventModel(data=data)

    async def _get_wiki_response(self) -> dict:
        century = self._year_to_century_converter(self._year)
        return await query_century(century, self._lang)


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
