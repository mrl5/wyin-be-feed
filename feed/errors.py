# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


class WyinFeedBaseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class FutureYearError(WyinFeedBaseError):
    def __init__(self, msg):
        self.msg = msg


class BeforeCommonEraError(WyinFeedBaseError):
    def __init__(self, msg):
        self.msg = msg


class NoContentError(WyinFeedBaseError):
    def __init__(self, msg):
        self.msg = msg


class UnsupportedLanguageError(WyinFeedBaseError):
    def __init__(self, msg):
        self.msg = msg
