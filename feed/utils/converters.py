# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from roman import toRoman

from feed.errors import BeforeCommonEraError, FutureYearError


def convert_time_to_year(time: str) -> int:
    year = int(time.replace(":", ""))
    throw_on_invalid_year(year)
    return year


def convert_year_to_century(year: int) -> str:
    throw_on_invalid_year(year)
    century = -(-year // 100)
    century_roman = toRoman(century)
    return century_roman


def throw_on_invalid_year(year: int) -> None:
    assert year >= 0
    if year == 0:
        raise BeforeCommonEraError("this year is from before common era", year=year)
    if year > datetime.now().year:
        raise FutureYearError("this year is from future", year=year)
