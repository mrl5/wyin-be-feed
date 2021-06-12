# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from abc import ABCMeta
from enum import Enum, unique


class WyinFeedBaseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class NotFoundError(WyinFeedBaseError, metaclass=ABCMeta):
    def __init__(self, msg, year: int = None):
        self.year = year
        self.msg = msg
        self.code = NotFoundCodeEnum[self.__class__.__name__].value


@unique
class NotFoundCodeEnum(str, Enum):
    """
    Internal codes to distinguish reasons of 404
    """

    FutureYearError = "NF001"
    BeforeCommonEraError = "NF002"
    NoContentError = "NF003"


class FutureYearError(NotFoundError):
    ...


class BeforeCommonEraError(NotFoundError):
    ...


class NoContentError(NotFoundError):
    ...


class UnsupportedLanguageError(WyinFeedBaseError):
    def __init__(self, msg):
        self.msg = msg
