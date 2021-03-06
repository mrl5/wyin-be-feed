# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum, unique

from pydantic import BaseModel


@unique
class WikiTextExtractsEnum(str, Enum):
    """
    Possible Wikipedia TextExtracts
    https://www.mediawiki.org/wiki/Extension:TextExtracts
    """

    wiki_limited_html = "wiki_limited_html"
    wiki_plain_text = "wiki_plain_text"


class WikiUnprocessedModel(BaseModel):
    type: WikiTextExtractsEnum
    data: str
