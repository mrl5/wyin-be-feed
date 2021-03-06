# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from fastapi import Response


async def no_cache_headers(response: Response):
    response.headers["cache-control"] = "no-cache, no-store, must-revalidate, max-age=0"
