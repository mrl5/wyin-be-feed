# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from enum import Enum, unique
from pathlib import Path

CWD = Path(__file__).resolve().parent


@unique
class WikiResponseMocks(str, Enum):
    # https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&search=13
    en_wikidata_search_entities_year = "en_wikidata_api_wbsearchentities_year.json"
    pl_wikidata_search_entities_year = "pl_wikidata_api_wbsearchentities_year.json"
    pl_wikidata_search_entities_year_908 = (
        "pl_wikidata_api_wbsearchentities_year_908.json"
    )
    pl_wikidata_search_entities_year_912 = (
        "pl_wikidata_api_wbsearchentities_year_912.json"
    )
    pl_wikidata_search_entities_year_57 = (
        "pl_wikidata_api_wbsearchentities_year_57.json"
    )

    # https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&sitefilter=enwiki&ids=Q23411
    en_wikidata_get_entities_year = "en_wikidata_api_wbgetentities_year.json"
    pl_wikidata_get_entities_year = "pl_wikidata_api_wbgetentities_year.json"
    pl_wikidata_get_entities_year_908 = "pl_wikidata_api_wbgetentities_year_908.json"
    pl_wikidata_get_entities_year_912 = "pl_wikidata_api_wbgetentities_year_912.json"
    pl_wikidata_get_entities_year_57 = "pl_wikidata_api_wbgetentities_year_57.json"

    # https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles=AD%2013
    en_wiki_year = "en_wikipedia_api_year.json"
    pl_wiki_year = "pl_wikipedia_api_year.json"
    pl_wiki_year_912 = "pl_wikipedia_api_year_912.json"
    pl_wiki_year_57 = "pl_wikipedia_api_year_57.json"

    # https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=pl&search=X%20wiek
    pl_wikidata_search_entities_century = (
        "pl_wikidata_api_wbsearchentities_century.json"
    )
    pl_wikidata_search_entities_century_19 = (
        "pl_wikidata_api_wbsearchentities_century_19.json"
    )
    pl_wikidata_search_entities_century_1 = (
        "pl_wikidata_api_wbsearchentities_century_1.json"
    )

    # https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks&sitefilter=plwiki&ids=Q8052
    pl_wikidata_get_entities_century = "pl_wikidata_api_wbgetentities_century.json"
    pl_wikidata_get_entities_century_19 = (
        "pl_wikidata_api_wbgetentities_century_19.json"
    )
    pl_wikidata_get_entities_century_19bc = (
        "pl_wikidata_api_wbgetentities_century_19bc.json"
    )
    pl_wikidata_get_entities_century_1 = "pl_wikidata_api_wbgetentities_century_1.json"

    # https://pl.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&titles=X%20wiek
    pl_wiki_century = "pl_wikipedia_api_century.json"
    pl_wiki_century_1 = "pl_wikipedia_api_century_1.json"


@unique
class EventReponseMocks(str, Enum):
    pl_event = "pl_feed_event_sample_response.json"


def _json_to_dict(path: Path) -> dict:
    with open(path) as f:
        a_dict = json.load(f)
    return a_dict


def get_wiki_response(key: str) -> dict:
    path = CWD / WikiResponseMocks[key].value
    return _json_to_dict(path)


def get_event_response(key: str) -> dict:
    path = CWD / EventReponseMocks[key].value
    return _json_to_dict(path)
