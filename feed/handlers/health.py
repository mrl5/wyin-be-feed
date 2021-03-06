# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from feed.interfaces.handlers import IHttpRequestHandler
from feed.models.health import GenericHealthEnum, HealthModel


class Health(IHttpRequestHandler):
    def __init__(self):
        self._model = HealthModel()

    def _get_status(self) -> GenericHealthEnum:
        return GenericHealthEnum.healthy

    async def handle(self) -> HealthModel:
        self._model.status = self._get_status()
        return self._model
