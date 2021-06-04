# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import AsyncClient

from feed.handlers import history
from tests.mocks.fake_wikipedia_api import fake_app


def monkeypatch_history_event_handler(monkeypatch, force_timeout=False):
    def mockreturn():
        app = None if force_timeout else fake_app
        timeout = 0.0 if force_timeout else None
        return AsyncClient(app=app, timeout=timeout)

    monkeypatch.setattr(history, "get_async_client", mockreturn)
