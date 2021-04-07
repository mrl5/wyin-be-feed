# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

import roman

from feed.errors import BeforeCommonEraError, FutureYearError


def convert_time_to_year(time: str) -> int:
    year = int(time.replace(":", ""))
    if year > datetime.now().year:
        raise FutureYearError(f"this year is from future: {year}")
    return year


def convert_year_to_century(year: int) -> str:
    century = -(-year // 100)
    century_roman = roman.toRoman(century)

    if year == 0:
        raise BeforeCommonEraError(f"this year is from before common era")

    return century_roman
