# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.errors import BeforeCommonEraError, FutureYearError
from feed.utils.converters import convert_time_to_year, convert_year_to_century

time_year = [("10:00", 1000), ("8:13", 813), ("00:01", 1)]
unconvertable_times = [
    ("20:21", FutureYearError),
    ("20:22", FutureYearError),
    ("21:00", FutureYearError),
    ("10:20am", ValueError),
]

year_century = [(1000, "X"), (999, "X"), (1001, "XI"), (813, "IX"), (1, "I")]
year_century_exceptions = [(0, BeforeCommonEraError)]


@pytest.mark.parametrize("time, year", time_year)
def test_convert_time_to_year(time, year):
    assert convert_time_to_year(time) == year


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.parametrize("time, exception", unconvertable_times)
def test_convert_time_to_year_exceptions(time, exception):
    with pytest.raises(exception):
        convert_time_to_year(time)


@pytest.mark.parametrize("year, century", year_century)
def test_convert_year_to_century(year, century):
    assert convert_year_to_century(year) == century


@pytest.mark.parametrize("year, exception", year_century_exceptions)
def test_convert_year_to_century_exceptions(year, exception):
    with pytest.raises(exception):
        convert_year_to_century(year)
