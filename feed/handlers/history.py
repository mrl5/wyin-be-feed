# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from asyncio import gather
from time import strptime
from typing import Callable

from pydantic import BaseModel, validator

from feed.handlers.decorators import decode_request_params
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import (
    SingleHistoryEventModel,
    WikiTextExtractsEnum,
    WikiUnprocessedModel,
)
from feed.utils.converters import convert_time_to_year
from feed.utils.http_factory import get_async_client
from feed.utils.scrapers import (
    get_random_event_from_year_page,
    get_year_event_from_century_page,
)
from feed.utils.wikidata_api import (
    CenturyAndYearTitles,
    get_wikipedia_titles_for_century_and_year,
)
from feed.utils.wikipedia_api import get_wiki_page_content, query, query_year


class EventParams(BaseModel):
    t: str

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        strptime(v, "%H:%M")
        return v


class EventsParams(EventParams):
    ...


class Event(IHttpRequestHandler):
    _year: int
    _lang: str = "pl"

    @decode_request_params
    def __init__(self, params: dict):
        self._params = EventParams(**params)
        self._client = get_async_client()

    async def handle(self) -> SingleHistoryEventModel:
        self._year = convert_time_to_year(self._params.t)
        async with self._client:
            titles: CenturyAndYearTitles = await get_wikipedia_titles_for_century_and_year(
                self._year, self._lang, self._client
            )
            century_resp, year_resp = await gather(
                self._get_wiki_response(titles["century_title"]),
                self._get_wiki_response(titles["year_title"]),
            )

        data = self._get_historical_event(century_resp, year_resp)
        return SingleHistoryEventModel(data=data)

    async def _get_wiki_response(self, title: str) -> dict:
        response = await query(title, self._lang, self._client)
        return response.json()

    def _get_historical_event(self, century_resp: dict, year_resp: dict) -> str:
        html = get_wiki_page_content(century_resp)
        data = get_year_event_from_century_page(self._year, html)
        if data is not None:
            return data

        html = get_wiki_page_content(year_resp)
        data = get_random_event_from_year_page(html)
        return data


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
