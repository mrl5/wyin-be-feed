# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from feed.routers import health, history

app = FastAPI()

app.include_router(health.router)
app.include_router(history.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400, content={"detail": exc.errors(), "body": exc.body}
    )


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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="WYIN feed",
        version="0.1.0",
        description="WYIN feed API serving historical events",
        routes=app.routes,
    )
    return replace_false_422(openapi_schema, 400)


app.openapi = custom_openapi  # type: ignore
