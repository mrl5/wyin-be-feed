# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.errors import NoContentError
from feed.utils.scrapers import (
    get_random_event_from_year_page,
    get_year_event_from_century_page,
)
from feed.utils.wikipedia_api import get_wiki_page_content
from tests.mocks.mock_factory import get_wiki_response

mock_century_html = get_wiki_page_content(get_wiki_response("pl_wiki_century"))
mock_ambiguous_html = "<li>bitwa pod Stalingradem (1942–1943)</li><li>Lech Wałęsa (ur. 1943) – prezydent RP</li>"
mock_regex_hell_1_html = "<li>1206 – Temudżyn (Czyngis-chan) zjednoczył Mongołów i rozpoczął podboje (pd. Syberia w 1207, pn. Chiny w 1211, wsch. Iran w 1218)</li>\n<li>1207 – doszło do wielkiego pożaru Magdeburga w wyniku którego m.in. spłonęła doszczętnie miejscowa katedra (20 kwietnia)</li><li>1211 – Alfons II został królem Portugalii (26 marca)</li><li>1218 – św. Piotr Nolasco założył w Barcelonie Zakon Najświętszej Maryi Panny Miłosierdzia dla Odkupienia Niewolników (10 sierpnia)</li>"
mock_regex_hell_2_html = "<ul><li>1301 - papież Bonifacy VIII wydał bullę <i>Ausculta fili carissime</i>, w której zagroził ekskomuniką królowi Francji Filipowi IV, w związku z nałożeniem przez niego podatku na duchownych i przejęcie sądów nad nimi (5 grudnia)</li>\n<li>1302 - Dante Alighieri został skazany na wygnanie z Florencji (27 stycznia)</li></ul>"
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
    (
        1206,
        "1206 – Temudżyn (Czyngis-chan) zjednoczył Mongołów i rozpoczął podboje (pd. Syberia w 1207, pn. Chiny w 1211, wsch. Iran w 1218)",
        mock_regex_hell_1_html,
    ),
    (
        1207,
        "1207 – doszło do wielkiego pożaru Magdeburga w wyniku którego m.in. spłonęła doszczętnie miejscowa katedra (20 kwietnia)",
        mock_regex_hell_1_html,
    ),
    (
        1211,
        "1211 – Alfons II został królem Portugalii (26 marca)",
        mock_regex_hell_1_html,
    ),
    (
        1218,
        "1218 – św. Piotr Nolasco założył w Barcelonie Zakon Najświętszej Maryi Panny Miłosierdzia dla Odkupienia Niewolników (10 sierpnia)",
        mock_regex_hell_1_html,
    ),
    (
        1301,
        "1301 - papież Bonifacy VIII wydał bullę Ausculta fili carissime, w której zagroził ekskomuniką królowi Francji Filipowi IV, w związku z nałożeniem przez niego podatku na duchownych i przejęcie sądów nad nimi (5 grudnia)",
        mock_regex_hell_2_html,
    ),
    (1942, "bitwa pod Stalingradem (1942–1943)", mock_ambiguous_html),
    (1943, "Lech Wałęsa (ur. 1943) – prezydent RP", mock_ambiguous_html),
]

random_event_cases = (
    get_wiki_page_content(get_wiki_response("pl_wiki_year")),
    get_wiki_page_content(get_wiki_response("pl_wiki_year_912")),
    '<h2><span id="Wydarzenia">Wydarzenia</span></h2>\n<ul><li><b>Europa</b>\n<ul><li>założono zakon benedyktynów</li>\n<li>Anastazjusz zbudował fortyfikacje przeciw Słowianom</li></ul></li></ul><h2><span id="Urodzili_si.C4.99"></span><span id="Urodzili_się">Urodzili się</span></h2>\n<ul><li><span><i>Brak danych.</i></span></li></ul><h2><span id="Zmarli">Zmarli</span></h2>\n<ul><li class="mw-empty-elt"></ul><p><br></p>',
)


@pytest.mark.parametrize("year, event, century_page", year_events)
def test_get_year_event_from_century_page(year, event, century_page):
    assert get_year_event_from_century_page(year, century_page) == event


@pytest.mark.parametrize("html", random_event_cases)
def test_get_random_event_from_year_page(html):
    results = [get_random_event_from_year_page(html) for _ in range(100)]

    assert all([r == results[0] for r in results]) is False
    assert all([r != "Brak danych." for r in results]) is True


def test_get_random_event_from_year_page_exceptions():
    html = get_wiki_page_content(get_wiki_response("pl_wiki_year_57"))
    with pytest.raises(NoContentError):
        get_random_event_from_year_page(html)
