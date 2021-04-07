# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.utils.scrapers import get_year_event_from_century_page
from feed.utils.wikipedia_api import get_wiki_page_content
from tests.mocks.mock_factory import get_wiki_response

mock_html = get_wiki_page_content(get_wiki_response("pl_wiki_century"))
year_events = [
    (908, "908 - w Bagdadzie odnotowano opady śniegu", mock_html),
    (
        909,
        "909/910 - powstało opactwo św. Piotra i Pawła w Cluny we Francji",
        mock_html,
    ),
    (
        910,
        "910 - książę Wilhelm Akwitański założył benedyktyńskie opactwo w Cluny",
        mock_html,
    ),
    (911, None, mock_html),
    (912, None, mock_html),
]


@pytest.mark.parametrize("year, event, century_page", year_events)
def test_get_year_event_from_century_page(year, event, century_page):
    assert get_year_event_from_century_page(year, century_page) == event
