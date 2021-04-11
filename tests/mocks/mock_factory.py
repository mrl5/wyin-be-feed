# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from enum import Enum, unique
from pathlib import Path

from httpx import AsyncClient

from feed.handlers.history import Event, Events
from feed.utils.wikipedia_api import query_century, query_year

CWD = Path(__file__).resolve().parent


@unique
class WikiResponseMocks(str, Enum):
    # https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&search=13
    en_wikidata_search_entities = "en_wikidata_api_wbsearchentities.json"
    pl_wikidata_search_entities = "pl_wikidata_api_wbsearchentities.json"

    # https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&sitefilter=enwiki&ids=Q23411
    en_wikidata_get_entities = "en_wikidata_api_wbgetentities.json"
    pl_wikidata_get_entities = "pl_wikidata_api_wbgetentities.json"

    # https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles=AD%2013
    en_wiki = "en_wikipedia_api_sample_response.json"
    pl_wiki = "pl_wikipedia_api_sample_response.json"

    # https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=pl&search=X%20wiek
    pl_wikidata_search_entities_century = (
        "pl_wikidata_api_wbsearchentities_century.json"
    )
    pl_wikidata_search_entities_century_19 = (
        "pl_wikidata_api_wbsearchentities_century_19.json"
    )
    # https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&sitefilter=plwiki&ids=Q8052
    pl_wikidata_get_entities_century = "pl_wikidata_api_wbgetentities_century.json"
    pl_wikidata_get_entities_century_19 = (
        "pl_wikidata_api_wbgetentities_century_19.json"
    )
    pl_wikidata_get_entities_century_19bc = (
        "pl_wikidata_api_wbgetentities_century_19bc.json"
    )
    # https://pl.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles=X%20wiek
    pl_wiki_century = "pl_wikipedia_api_century.json"


@unique
class EventReponseMocks(str, Enum):
    pl_event = "pl_feed_event_sample_response.json"


@unique
class EventsReponseMocks(str, Enum):
    pl_events = "pl_feed_events_sample_response.json"


def _json_to_dict(path: Path) -> dict:
    with open(path) as f:
        a_dict = json.load(f)
    return a_dict


def get_wiki_response(key: str) -> dict:
    path = CWD / WikiResponseMocks[key].value
    return _json_to_dict(path)


def get_event_response(key: str) -> dict:
    path = CWD / EventReponseMocks[key].value
    return _json_to_dict(path)


def get_events_response(key: str) -> dict:
    path = CWD / EventsReponseMocks[key].value
    return _json_to_dict(path)


def monkeypatch_history_event_handler(monkeypatch, force_timeout=False):
    async def mockreturn(self):
        self._time_to_year_converter(self._params.t)
        if force_timeout:
            lang = "pl"
            client = AsyncClient(app=None, timeout=0.0)
            async with client:
                return await query_century("X", lang, client)
        return get_wiki_response("pl_wiki_century")

    monkeypatch.setattr(Event, "_get_wiki_response", mockreturn)


def monkeypatch_history_events_handler(monkeypatch, force_timeout=False):
    async def mockreturn(self):
        self._time_to_year_converter(self._params.t)
        if force_timeout:
            lang = "pl"
            client = AsyncClient(app=None, timeout=0.0)
            async with client:
                return await query_year("1000", lang, client)
        return get_wiki_response("pl_wiki")

    monkeypatch.setattr(Events, "_get_wiki_response", mockreturn)
