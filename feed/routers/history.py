# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import APIRouter, Depends, Response

from feed.dependencies import no_cache_headers
from feed.handlers.health import Health
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.health import HealthModel

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/events")
async def get_events():
    pass
