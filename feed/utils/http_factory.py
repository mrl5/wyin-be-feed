# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import AsyncClient

from feed.conf import HTTP_REQUEST_TIMEOUT


def get_async_client():
    client = AsyncClient(timeout=HTTP_REQUEST_TIMEOUT)
    return client
