# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import FastAPI

from tests.mocks.mock_factory import get_wiki_response

fake_app = FastAPI()


WIKIDATA_ACTIONS = ["wbsearchentities", "wbgetentities"]


@fake_app.get("/w/api.php")
async def wiki_api(language: str, action: str, search: str = None, ids: str = None):
    if action == "wbsearchentities":
        if language == "pl" and search is not None and search.endswith("wiek"):
            if search == "XIX wiek":
                return get_wiki_response(
                    f"{language}_wikidata_search_entities_century_19"
                )
            return get_wiki_response(f"{language}_wikidata_search_entities_century")
        return get_wiki_response(f"{language}_wikidata_search_entities")

    elif action == "wbgetentities":
        if ids == "Q8052":
            return get_wiki_response(f"{language}_wikidata_get_entities_century")
        if ids == "Q6955":
            return get_wiki_response(f"{language}_wikidata_get_entities_century_19")
        if ids == "Q186674":
            return get_wiki_response(f"{language}_wikidata_get_entities_century_19bc")
        return get_wiki_response(f"{language}_wikidata_get_entities")

    raise NotImplementedError(f"this action is not supported: {action}")
