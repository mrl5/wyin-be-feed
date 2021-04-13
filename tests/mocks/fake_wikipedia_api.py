# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import FastAPI

from tests.mocks.fake_wikidata_api import WIKIDATA_ACTIONS
from tests.mocks.fake_wikidata_api import wiki_api as wikidata_api
from tests.mocks.mock_factory import get_wiki_response

fake_app = FastAPI()


@fake_app.get("/w/api.php")
async def wiki_api(
    lang: str = "pl",
    action: str = None,
    titles: str = None,
    search: str = None,
    ids: str = None,
):
    if action in WIKIDATA_ACTIONS:
        return await wikidata_api(lang, action, search, ids)

    if lang == "pl" and titles is not None and titles.endswith("wiek"):
        return get_wiki_response(f"{lang}_wiki_century")

    if lang == "pl" and titles is not None and titles == "912":
        return get_wiki_response(f"{lang}_wiki_year_912")

    return get_wiki_response(f"{lang}_wiki_year")
