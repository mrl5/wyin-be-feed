# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import AsyncClient

from feed.handlers.history import Event, Events
from feed.utils.wikipedia_api import query_year
from tests.mocks.fake_wikipedia_api import fake_app
from tests.mocks.mock_factory import get_wiki_response


def monkeypatch_history_event_handler(monkeypatch, force_timeout=False):
    app = None if force_timeout else fake_app
    timeout = 0.0 if force_timeout else None
    client = AsyncClient(app=app, timeout=timeout)
    monkeypatch.setattr(Event, "_client", client)


def monkeypatch_history_events_handler(monkeypatch, force_timeout=False):
    # todo improve like above
    async def mockreturn(self):
        self._time_to_year_converter(self._params.t)
        if force_timeout:
            lang = "pl"
            client = AsyncClient(app=None, timeout=0.0)
            async with client:
                return await query_year("1000", lang, client)
        return get_wiki_response("pl_wiki_year")

    monkeypatch.setattr(Events, "_get_wiki_response", mockreturn)
