# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from httpx import URL, AsyncClient, Response

DEFAULT_LANG = "pl"


async def query(year: int, lang: str = None, client: AsyncClient = None) -> Response:
    lang = lang if lang is not None else DEFAULT_LANG
    client = client if client is not None else AsyncClient()

    client.base_url = URL(f"https://{lang}.wikipedia.org")
    client.params.update({"action": "query", "prop": "extracts", "format": "json"})
    return await client.get("/w/api.php", params={"titles": year})
