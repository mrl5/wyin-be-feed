# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import APIRouter, Depends, Response

from app.dependencies import no_cache_headers
from app.handlers.health import Health
from app.interfaces.handlers import IHttpRequestHandler
from app.models.health import HealthModel

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/events")
async def get_events():
	pass