# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from feed.errors import NotFoundError
from feed.handlers.history import Event, EventRandom
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import NotFoundModel, SingleHistoryEventModel

router = APIRouter(prefix="/history", tags=["history"])


@router.get(
    "/event",
    response_model=SingleHistoryEventModel,
    responses={404: {"model": NotFoundModel}},
)
async def get_event(
    t: str = Query(
        ...,
        regex="^[0-9]{1,2}(:|%3A)[0-9]{2}$",
        title="time",
        description="24-hour clock time in %H:%M format",
    )
):
    h: IHttpRequestHandler = Event(locals())
    try:
        return await h.handle()
    except NotFoundError as nfe:
        content = NotFoundModel(body=str(nfe), code=nfe.code).json()
        return JSONResponse(status_code=404, content=content)


@router.get(
    "/event/random",
    response_model=SingleHistoryEventModel,
    responses={404: {"model": NotFoundModel}},
)
async def get_event_random():
    h: IHttpRequestHandler = EventRandom()
    try:
        return await h.handle()
    except NotFoundError as nfe:
        content = NotFoundModel(body=str(nfe), code=nfe.code).json()
        return JSONResponse(status_code=404, content=content)
