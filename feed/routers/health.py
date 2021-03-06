# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import APIRouter, Depends, Response

from feed.dependencies import no_cache_headers
from feed.handlers.health import Health
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.health import HealthModel

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthModel)
async def get_health(response: Response = Depends(no_cache_headers)):
    h: IHttpRequestHandler = Health()
    return await h.handle()
