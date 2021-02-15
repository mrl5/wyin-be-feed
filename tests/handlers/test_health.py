# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from app.handlers.health import Health
from app.interfaces.handlers import IHttpRequestHandler
from app.models.health import GenericHealthEnum, HealthModel


@pytest.fixture(scope="function")
def instance():
    o = Health()
    return o


def test_interface(instance):
    assert isinstance(instance, IHttpRequestHandler)


def test_health_check(instance):
    assert instance.handle().status == GenericHealthEnum.healthy
