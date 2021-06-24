# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os import environ

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from httpx import TimeoutException

from feed.conf import ALLOWED_ORIGINS
from feed.errors import UnsupportedLanguageError
from feed.routers import health, history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(history.router)


@app.exception_handler(RequestValidationError)
@app.exception_handler(UnsupportedLanguageError)
async def request_validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"body": "Bad Request"})


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400, content={"body": next(iter(exc.errors()))["msg"]}
    )


@app.exception_handler(TimeoutException)
async def timeout_exception_handler(request, exc):
    return JSONResponse(status_code=504, content={"body": str(exc)})


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


def get_version():
    if "API_VERSION" in environ:
        return environ["API_VERSION"]
    else:
        print("zonk")
        return "latest"


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="WYIN feed",
        version=get_version(),
        description="WYIN feed API serving historical events",
        routes=app.routes,
    )
    return replace_false_422(openapi_schema, 400)


app.openapi = custom_openapi  # type: ignore
