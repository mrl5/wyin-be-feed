# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from abc import abstractmethod

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import runtime_checkable, Protocol

from pydantic import BaseModel


@runtime_checkable
class IHttpRequestHandler(Protocol):
    # design pattern: command
    @abstractmethod
    def handle(self) -> BaseModel:
        raise NotImplementedError
