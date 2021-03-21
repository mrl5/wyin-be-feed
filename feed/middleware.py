# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from feed.errors import FutureYearError


async def catch_exceptions_middleware(request: Request, call_next):
    # https://github.com/tiangolo/fastapi/issues/775
    try:
        return await call_next(request)
    except ValidationError as ve:
        return JSONResponse(
            status_code=400, content={"body": next(iter(ve.errors()))["msg"]}
        )
    except FutureYearError as fye:
        return JSONResponse(status_code=404, content={"body": str(fye)})
    except Exception:
        return JSONResponse(status_code=500, content={"body": "Internal server error"})


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
