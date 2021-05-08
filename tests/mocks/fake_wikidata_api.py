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
            if search == "I wiek":
                return get_wiki_response(
                    f"{language}_wikidata_search_entities_century_1"
                )
            return get_wiki_response(f"{language}_wikidata_search_entities_century")

        if language == "pl" and search is not None and search == "908":
            return get_wiki_response(f"{language}_wikidata_search_entities_year_908")

        if language == "pl" and search is not None and search == "912":
            return get_wiki_response(f"{language}_wikidata_search_entities_year_912")

        if language == "pl" and search is not None and search == "57":
            return get_wiki_response(f"{language}_wikidata_search_entities_year_57")

        return get_wiki_response(f"{language}_wikidata_search_entities_year")

    elif action == "wbgetentities":
        if ids == "Q8052":
            return get_wiki_response(f"{language}_wikidata_get_entities_century")

        if ids == "Q6955":
            return get_wiki_response(f"{language}_wikidata_get_entities_century_19")

        if ids == "Q186674":
            return get_wiki_response(f"{language}_wikidata_get_entities_century_19bc")

        if ids == "Q8106":
            return get_wiki_response(f"{language}_wikidata_get_entities_century_1")

        if ids == "Q23837":
            return get_wiki_response(f"{language}_wikidata_get_entities_year_912")

        if ids == "Q30969":
            return get_wiki_response(f"{language}_wikidata_get_entities_year_57")

        if ids == "Q8052|Q30463":
            Q8052 = get_wiki_response(f"{language}_wikidata_get_entities_century")[
                "entities"
            ]
            Q30463 = get_wiki_response(f"{language}_wikidata_get_entities_year_908")[
                "entities"
            ]
            return {"entities": {**Q8052, **Q30463}}

        if ids == "Q8052|Q23411":
            Q8052 = get_wiki_response(f"{language}_wikidata_get_entities_century")[
                "entities"
            ]
            Q23411 = get_wiki_response(f"{language}_wikidata_get_entities_year")[
                "entities"
            ]
            return {"entities": {**Q8052, **Q23411}}

        if ids == "Q8052|Q23837":
            Q8052 = get_wiki_response(f"{language}_wikidata_get_entities_century")[
                "entities"
            ]
            Q23837 = get_wiki_response(f"{language}_wikidata_get_entities_year_912")[
                "entities"
            ]
            return {"entities": {**Q8052, **Q23837}}

        if ids == "Q8106|Q30969":
            Q8106 = get_wiki_response(f"{language}_wikidata_get_entities_century_1")[
                "entities"
            ]
            Q30969 = get_wiki_response(f"{language}_wikidata_get_entities_year_57")[
                "entities"
            ]
            return {"entities": {**Q8106, **Q30969}}

        return get_wiki_response(f"{language}_wikidata_get_entities_year")

    raise NotImplementedError(f"this action is not supported: {action}")
