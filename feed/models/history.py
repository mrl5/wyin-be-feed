# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from pydantic import BaseModel

from feed.errors import NotFoundCodeEnum


class SingleHistoryEventModel(BaseModel):
    year: int
    data: str
    category: Optional[str]
    source: str


class NotFoundModel(BaseModel):
    year: int
    body: str
    code: NotFoundCodeEnum
