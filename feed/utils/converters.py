# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from feed.errors import FutureYearError


def convert_time_to_year(time: str) -> int:
    year = int(time.replace(":", ""))
    if year > datetime.now().year:
        raise FutureYearError(f"this year is from future: {year}")
    return year
