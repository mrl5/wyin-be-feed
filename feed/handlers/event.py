# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABCMeta
from asyncio import gather
from typing import Optional
from urllib.parse import quote

from pydantic import BaseModel, validator

from feed.conf import DEFAULT_LANGUAGE
from feed.errors import NotFoundError
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import SingleHistoryEventModel
from feed.utils.http_factory import get_async_client
from feed.utils.scrapers import (
    EventAndCategory,
    get_random_event_from_year_page,
    get_year_event_from_century_page,
)
from feed.utils.wikidata_api import (
    CenturyAndYearTitles,
    get_wikipedia_titles_for_century_and_year,
    throw_on_unsupported_language,
)
from feed.utils.wikipedia_api import get_wiki_page_content, query


class EventParams(BaseModel):
    lang: str = DEFAULT_LANGUAGE

    @validator("lang")
    def lang_supported_by_wikipedia(cls, lang):
        throw_on_unsupported_language(lang)
        return lang


class Event(IHttpRequestHandler, metaclass=ABCMeta):
    _year: int
    _lang: str = DEFAULT_LANGUAGE

    def __init__(self, params: dict = {}):
        self._client = get_async_client()
        self._params = EventParams(**params)

    async def handle(self) -> SingleHistoryEventModel:
        self._lang = self._params.lang
        async with self._client:
            titles: CenturyAndYearTitles = await get_wikipedia_titles_for_century_and_year(
                self._year, self._lang, self._client
            )
            century_resp, year_resp = await gather(
                self._get_wiki_response(titles.century_title),
                self._get_wiki_response(titles.year_title),
            )

        event = self._get_historical_event(century_resp, year_resp, titles)
        return SingleHistoryEventModel(
            year=self._year,
            data=event["data"],
            category=event["category"],
            source=event["source"],
        )

    async def _get_wiki_response(self, title: str) -> dict:
        response = await query(title, self._lang, self._client)
        return response.json()

    def _get_historical_event(
        self, century_resp: dict, year_resp: dict, titles: CenturyAndYearTitles
    ) -> dict:
        html = get_wiki_page_content(century_resp)
        data: Optional[EventAndCategory] = get_year_event_from_century_page(
            self._year, html
        )
        if data is not None:
            source = self._get_source(titles.century_title)
            return {"data": data.event, "category": data.category, "source": source}

        html = get_wiki_page_content(year_resp)
        try:
            data = get_random_event_from_year_page(html)
        except NotFoundError as nfe:
            nfe.year = self._year
            raise nfe
        source = self._get_source(titles.year_title)
        return {"data": data.event, "category": data.category, "source": source}

    def _get_source(self, title: str) -> str:
        encoded_title = quote(title)
        return f"https://{self._lang}.wikipedia.org/wiki/{encoded_title}"
