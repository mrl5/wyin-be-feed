# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.utils.scrapers import (
    get_random_event_from_year_page,
    get_year_event_from_century_page,
)
from feed.utils.wikipedia_api import get_wiki_page_content
from tests.mocks.mock_factory import get_wiki_response

mock_century_html = get_wiki_page_content(get_wiki_response("pl_wiki_century"))
mock_ambiguous_html = "<li>bitwa pod Stalingradem (1942–1943)</li><li>Lech Wałęsa (ur. 1943) – prezydent RP</li>"
year_events = [
    (908, "908 - w Bagdadzie odnotowano opady śniegu", mock_century_html),
    (
        909,
        "909/910 - powstało opactwo św. Piotra i Pawła w Cluny we Francji",
        mock_century_html,
    ),
    (
        910,
        "910 - książę Wilhelm Akwitański założył benedyktyńskie opactwo w Cluny",
        mock_century_html,
    ),
    (911, None, mock_century_html),
    (912, None, mock_century_html),
    (1942, "bitwa pod Stalingradem (1942–1943)", mock_ambiguous_html),
    (1943, "Lech Wałęsa (ur. 1943) – prezydent RP", mock_ambiguous_html),
]

random_event_cases = (
    get_wiki_page_content(get_wiki_response("pl_wiki_year")),
    get_wiki_page_content(get_wiki_response("pl_wiki_year_912")),
)


@pytest.mark.parametrize("year, event, century_page", year_events)
def test_get_year_event_from_century_page(year, event, century_page):
    assert get_year_event_from_century_page(year, century_page) == event


@pytest.mark.parametrize("html", random_event_cases)
def test_get_random_event_from_year_page(html):
    results = []
    for _ in range(100):
        results.append(get_random_event_from_year_page(html))

    assert all([result == results[0] for result in results]) is False
    assert all([result != "Brak danych." for result in results]) is True
