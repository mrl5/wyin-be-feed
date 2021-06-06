# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pydantic import BaseModel

from feed.errors import NotFoundCodeEnum


class SingleHistoryEventModel(BaseModel):
    data: str
    source: str


class NotFoundModel(BaseModel):
    body: str
    code: NotFoundCodeEnum
