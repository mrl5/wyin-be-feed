# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from random import choice

from httpx import AsyncClient

from feed.handlers import history
from feed.handlers.history import EventRandom
from tests.mocks.fake_wikipedia_api import fake_app


def monkeypatch_history_event_handler(monkeypatch, force_timeout=False):
    _monkeypatch_async_client(monkeypatch, force_timeout)


def monkeypatch_history_event_random_handler(monkeypatch, force_timeout=False):
    def mockreturn(self):
        mocked_years = [912, 1020]
        return choice(mocked_years)

    _monkeypatch_async_client(monkeypatch, force_timeout)
    monkeypatch.setattr(EventRandom, "_get_random_year", mockreturn)


def _monkeypatch_async_client(monkeypatch, force_timeout=False):
    def mockreturn():
        app = None if force_timeout else fake_app
        timeout = 0.0 if force_timeout else None
        return AsyncClient(app=app, timeout=timeout)

    monkeypatch.setattr(history, "get_async_client", mockreturn)
