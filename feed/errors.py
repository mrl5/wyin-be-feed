# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


class FutureYearError(Exception):
    def __init__(self, msg):
        self.msg = msg


class BeforeCommonEraError(Exception):
    def __init__(self, msg):
        self.msg = msg


class UnsupportedLanguageError(Exception):
    def __init__(self, msg):
        self.msg = msg
