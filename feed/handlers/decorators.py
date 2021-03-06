# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from functools import wraps
from urllib.parse import unquote


def decode_request_params(f):
    def get_decoded_dict(a_dict: dict) -> dict:
        return {k: unquote(v) for k, v in a_dict.items()}

    @wraps(f)
    def wrapper(*args, **kwargs):
        decoded_args = [get_decoded_dict(a) if isinstance(a, dict) else a for a in args]
        decoded_kwargs = {
            k: get_decoded_dict(v) if isinstance(v, dict) else v
            for k, v in kwargs.items()
        }
        return f(*decoded_args, **decoded_kwargs)

    return wrapper
