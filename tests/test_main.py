# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from fastapi.testclient import TestClient

from app.main import app

# https://opensource.zalando.com/restful-api-guidelines/#227
NO_CACHE_HEADERS = "no-cache, no-store, must-revalidate, max-age=0"


@pytest.fixture(scope="function")
def client():
    client = TestClient(app)
    return client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["cache-control"] == NO_CACHE_HEADERS
