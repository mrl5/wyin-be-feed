# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.handlers.health import Health
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.health import GenericHealthEnum


@pytest.fixture(scope="function")
def instance():
    o = Health()
    return o


def test_interface(instance):
    assert isinstance(instance, IHttpRequestHandler)


@pytest.mark.asyncio
async def test_health_check(instance):
    result = await instance.handle()
    assert result.status == GenericHealthEnum.healthy
