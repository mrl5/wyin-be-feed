# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from asyncio import gather
from datetime import datetime
from random import randrange
from time import strptime
from urllib.parse import quote

from pydantic import BaseModel, validator

from feed.conf import DEFAULT_LANGUAGE
from feed.errors import NotFoundError
from feed.handlers.decorators import decode_request_params
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import SingleHistoryEventModel
from feed.utils.converters import convert_time_to_year, throw_on_invalid_year
from feed.utils.http_factory import get_async_client
from feed.utils.scrapers import (
    get_random_event_from_year_page,
    get_year_event_from_century_page,
)
from feed.utils.wikidata_api import (
    CenturyAndYearTitles,
    get_wikipedia_titles_for_century_and_year,
    throw_on_unsupported_language,
)
from feed.utils.wikipedia_api import get_wiki_page_content, query


class _Event(IHttpRequestHandler):
    _year: int
    _lang: str = DEFAULT_LANGUAGE

    def __init__(self):
        self._client = get_async_client()

    async def handle(self) -> SingleHistoryEventModel:
        async with self._client:
            titles: CenturyAndYearTitles = await get_wikipedia_titles_for_century_and_year(
                self._year, self._lang, self._client
            )
            century_resp, year_resp = await gather(
                self._get_wiki_response(titles["century_title"]),
                self._get_wiki_response(titles["year_title"]),
            )

        event = self._get_historical_event(century_resp, year_resp, titles)
        return SingleHistoryEventModel(
            year=self._year, data=event["data"], source=event["source"]
        )

    async def _get_wiki_response(self, title: str) -> dict:
        response = await query(title, self._lang, self._client)
        return response.json()

    def _get_historical_event(
        self, century_resp: dict, year_resp: dict, titles: CenturyAndYearTitles
    ) -> dict:
        html = get_wiki_page_content(century_resp)
        data = get_year_event_from_century_page(self._year, html)
        if data is not None:
            source = self._get_source(titles["century_title"])
            return {"data": data, "source": source}

        html = get_wiki_page_content(year_resp)
        try:
            data = get_random_event_from_year_page(html)
        except NotFoundError as nfe:
            nfe.year = self._year
            raise nfe
        source = self._get_source(titles["year_title"])
        return {"data": data, "source": source}

    def _get_source(self, title: str) -> str:
        encoded_title = quote(title)
        return f"https://{self._lang}.wikipedia.org/wiki/{encoded_title}"


class EventParams(BaseModel):
    t: str
    lang: str = DEFAULT_LANGUAGE

    @validator("t")
    def time_in_24_hour_clock_format(cls, v):
        strptime(v, "%H:%M")
        return v

    @validator("lang")
    def lang_supported_by_wikipedia(cls, lang):
        throw_on_unsupported_language(lang)
        return lang


class EventRandomParams(BaseModel):
    lang: str = DEFAULT_LANGUAGE

    @validator("lang")
    def lang_supported_by_wikipedia(cls, lang):
        throw_on_unsupported_language(lang)
        return lang


class EventYearParams(BaseModel):
    year: int
    lang: str = DEFAULT_LANGUAGE

    @validator("year")
    def valid_year(cls, v):
        y = int(v)
        throw_on_invalid_year(y)
        return y

    @validator("lang")
    def lang_supported_by_wikipedia(cls, lang):
        throw_on_unsupported_language(lang)
        return lang


class Event(_Event):
    @decode_request_params
    def __init__(self, params: dict):
        super().__init__()
        self._params = EventParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = convert_time_to_year(self._params.t)
        self._lang = self._params.lang
        return await super().handle()


class EventRandom(_Event):
    @decode_request_params
    def __init__(self, params: dict = {}):
        super().__init__()
        self._params = EventRandomParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = self._get_random_year()
        self._lang = self._params.lang
        return await super().handle()

    def _get_random_year(self) -> int:
        return randrange(1, datetime.now().year)


class EventYear(_Event):
    @decode_request_params
    def __init__(self, params: dict):
        super().__init__()
        self._params = EventYearParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._year = self._params.year
        self._lang = self._params.lang
        return await super().handle()
