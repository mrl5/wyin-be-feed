# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from feed.errors import FutureYearError
from feed.utils.converters import convert_time_to_year

time_year = [("10:00", 1000), ("8:13", 813), ("00:01", 1)]
unconvertable_times = [
    ("20:21", FutureYearError),
    ("20:22", FutureYearError),
    ("21:00", FutureYearError),
    ("10:20am", ValueError),
]


@pytest.mark.parametrize("time, year", time_year)
def test_convert_time_to_year(time, year):
    assert convert_time_to_year(time) == year


@pytest.mark.freeze_time("2020-01-01")
@pytest.mark.parametrize("time, exception", unconvertable_times)
def test_convert_time_to_year_exceptions(time, exception):
    with pytest.raises(exception):
        convert_time_to_year(time)
