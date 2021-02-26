# SPDX-License-Identifier: MPL-2.0
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from app.interfaces.handlers import IHttpRequestHandler
from app.models.health import GenericHealthEnum, HealthModel


class Health(IHttpRequestHandler):
    def __init__(self):
        self._model = HealthModel()

    def _get_status(self) -> GenericHealthEnum:
        return GenericHealthEnum.healthy

    def handle(self) -> HealthModel:
        self._model.status = self._get_status()
        return self._model
