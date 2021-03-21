# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import APIRouter, Query

from feed.handlers.history import Events
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import WikiUnprocessedModel

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/events", response_model=WikiUnprocessedModel)
async def get_events(
    t: str = Query(
        ...,
        regex="^[0-9]{1,2}(:|%3A)[0-9]{2}$",
        title="time",
        description="24-hour clock time in %H:M% format",
    )
):
    h: IHttpRequestHandler = Events(locals())
    return await h.handle()
