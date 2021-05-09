# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from random import choice
from typing import Iterator, Optional

from bs4 import BeautifulSoup
from bs4.element import NavigableString

from feed.errors import NoContentError


def get_year_event_from_century_page(year: int, century_page: str) -> Optional[str]:
    soup = BeautifulSoup(century_page, features="html.parser")
    year_first_pattern = re.compile(
        rf"""        # https://www.python.org/dev/peps/pep-0498/#raw-f-strings
        ^            # start of string (see: https://www.regular-expressions.info/anchors.html)
        {str(year)}  # injected year variable as f-string
    """,
        re.VERBOSE,  # https://docs.python.org/3/library/re.html#re.VERBOSE
    )
    year_later_pattern = re.compile(
        rf"""
        [^/\-\–]     # negated characters (see: https://www.regular-expressions.info/charclass.html)
        {str(year)}
    """,
        re.VERBOSE,
    )

    tags = [
        soup.find(name="li", string=year_first_pattern),
        soup.find(name="li", string=year_later_pattern),
        soup.find(name="li"),  # workaround due to strange bs4 bug
    ]

    for tag in tags:
        if tag is not None:
            text = tag.get_text()
            condition_for_none = text.endswith(" -") or str(year) not in text
            return None if condition_for_none else text
    return None


def get_random_event_from_year_page(year_page: str) -> str:
    soup = BeautifulSoup(year_page, features="html.parser")
    tags = soup.find_all(name="li")
    leaf_tags = [
        tag for tag in tags if isinstance(safe_next(tag.children), NavigableString)
    ]

    if len(leaf_tags) == 0:
        raise NoContentError("no content for given year")
    return choice(leaf_tags).get_text()


def safe_next(iterator: Iterator[str]) -> Optional[str]:
    try:
        return next(iterator)
    except StopIteration:
        return None
