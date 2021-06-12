# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from feed.conf import DEFAULT_LANGUAGE
from feed.errors import NotFoundError
from feed.handlers.history import Event, EventRandom, EventYear
from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.history import NotFoundModel, SingleHistoryEventModel

router = APIRouter(prefix="/history", tags=["history"])

time_param = Query(
    ...,
    regex="^[0-9]{1,2}(:|%3A)[0-9]{2}$",
    title="time",
    description="24-hour clock time in %H:%M format",
)
lang_param = Query(
    DEFAULT_LANGUAGE,
    regex="^[-a-z]{2,12}$",
    title="language",
    description="language supported by wikipedia",
)


@router.get(
    "/event",
    response_model=SingleHistoryEventModel,
    responses={404: {"model": NotFoundModel}},
)
async def get_event(t: str = time_param, lang: Optional[str] = lang_param):
    try:
        h: IHttpRequestHandler = Event(locals())
        return await h.handle()
    except NotFoundError as nfe:
        content = NotFoundModel(body=str(nfe), code=nfe.code, year=nfe.year).dict()
        return JSONResponse(status_code=404, content=content)


@router.get(
    "/event/random",
    response_model=SingleHistoryEventModel,
    responses={404: {"model": NotFoundModel}},
)
async def get_event_random(lang: Optional[str] = lang_param):
    try:
        h: IHttpRequestHandler = EventRandom(locals())
        return await h.handle()
    except NotFoundError as nfe:
        content = NotFoundModel(body=str(nfe), code=nfe.code, year=nfe.year).dict()
        return JSONResponse(status_code=404, content=content)


@router.get(
    "/event/{year}",
    response_model=SingleHistoryEventModel,
    responses={404: {"model": NotFoundModel}},
)
async def get_event_year(year: int, lang: Optional[str] = lang_param):
    try:
        h: IHttpRequestHandler = EventYear(locals())
        return await h.handle()
    except NotFoundError as nfe:
        content = NotFoundModel(body=str(nfe), code=nfe.code, year=nfe.year).dict()
        return JSONResponse(status_code=404, content=content)
