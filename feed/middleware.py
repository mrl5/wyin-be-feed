# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import Response

from feed.errors import FutureYearError


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except FutureYearError as fye:
        return Response(str(fye), status_code=404)
    except Exception:
        return Response("Internal server error", status_code=500)


def replace_false_422(openapi_schema, true_status_code: int = 400):
    # https://github.com/tiangolo/fastapi/issues/1376
    for method in openapi_schema["paths"]:
        try:
            false_code = openapi_schema["paths"][method]["get"]["responses"]["422"]
            openapi_schema["paths"][method]["get"]["responses"][
                true_status_code
            ] = false_code
            del openapi_schema["paths"][method]["get"]["responses"]["422"]
        except KeyError:
            pass
    return openapi_schema
