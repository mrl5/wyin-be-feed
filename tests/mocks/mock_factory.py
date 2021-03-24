# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from enum import Enum, unique
from pathlib import Path

from httpx import AsyncClient

from feed.handlers.history import Events
from feed.utils.wikipedia_api import query_year

CWD = Path(__file__).resolve().parent


@unique
class WikiResponseMocks(str, Enum):
    en_wiki = "en_wikipedia_api_sample_response.json"
    pl_wiki = "pl_wikipedia_api_sample_response.json"


@unique
class EventsReponseMocks(str, Enum):
    en_events = "en_feed_events_sample_response.json"
    pl_events = "pl_feed_events_sample_response.json"


def _json_to_dict(path: Path) -> dict:
    with open(path) as f:
        a_dict = json.load(f)
    return a_dict


def get_wiki_response(key: str) -> dict:
    path = CWD / WikiResponseMocks[key].value
    return _json_to_dict(path)


def get_events_response(key: str) -> dict:
    path = CWD / EventsReponseMocks[key].value
    return _json_to_dict(path)


def monkeypatch_history_events_handler(monkeypatch, force_timeout=False):
    async def mockreturn(self):
        self._time_to_year_converter(self._params.t)
        if force_timeout:
            lang = "pl"
            client = AsyncClient(app=None, timeout=0.0)
            async with client:
                return await query_year("1000", lang, client)
        else:
            return get_wiki_response("pl_wiki")

    monkeypatch.setattr(Events, "_get_wiki_response", mockreturn)
