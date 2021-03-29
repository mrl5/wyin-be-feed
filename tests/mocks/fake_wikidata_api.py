# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import FastAPI

from tests.mocks.mock_factory import get_wiki_response

fake_app = FastAPI()


WIKIDATA_ACTIONS = ["wbsearchentities", "wbgetentities"]


@fake_app.get("/w/api.php")
async def wiki_api(language: str, action: str):
    if action == "wbsearchentities":
        return get_wiki_response(f"{language}_wikidata_search_entities")

    elif action == "wbgetentities":
        return get_wiki_response(f"{language}_wikidata_get_entities")

    raise NotImplementedError(f"this action is not supported: {action}")
