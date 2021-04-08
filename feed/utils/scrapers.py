# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from typing import Optional

from bs4 import BeautifulSoup


def get_year_event_from_century_page(year: int, century_page: str) -> Optional[str]:
    soup = BeautifulSoup(century_page, features="html.parser")
    pattern = re.compile(
        rf"""        # https://www.python.org/dev/peps/pep-0498/#raw-f-strings
        [^/]         # / is negated character (see: https://www.regular-expressions.info/charclass.html)
        {str(year)}  # injected year variable as f-string

        |            # https://www.regular-expressions.info/alternation.html

        ^            # start of string (see: https://www.regular-expressions.info/anchors.html)
        {str(year)}  # injected year variable as f-string
    """,
        re.VERBOSE,  # https://docs.python.org/3/library/re.html#re.VERBOSE
    )
    tag = soup.find(name="li", string=pattern)

    if tag is not None:
        text = tag.get_text()
        return None if text.endswith(" -") else text
    return None
