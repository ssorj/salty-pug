#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import logging
import os
import requests as _requests

_store_all_host = os.environ["STORE_SERVICE_HOST_ALL"]
_store_all_port = int(os.environ.get("STORE_SERVICE_PORT_ALL", 8080))
_store_all_url = f"http://{_store_all_host}:{_store_all_port}"

_factory_any_host = os.environ["FACTORY_SERVICE_HOST_ANY"]
_factory_any_port = int(os.environ.get("FACTORY_SERVICE_PORT_ANY", 8080))
_factory_any_url = f"http://{_factory_any_host}:{_factory_any_port}"

class Client:
    def find_items(self, product, size, color):
        data = _requests.get(f"{_store_all_url}/api/find-items").json()

        # Special case for non-aggregated result used in testing
        if isinstance(data, dict):
            data = [{"content": data}]

        results = list()

        # XXX Check for errors

        for response in data:
            results.extend(response["content"]["items"])

        return results, data # XXX

    def make_item(self, item, store):
        request_data = {
            "item": item.data(),
            "store_id": store.id,
        }

        response = _requests.post(f"{_factory_any_url}/api/make-item", json=request_data)

    def stock_item(self, item, store):
        request_data = {
            "item": item.data(),
        }

        store_host = os.environ.get("STORE_SERVICE_HOST_OVERRIDE", store.id)
        store_port = int(os.environ.get("STORE_SERVICE_PORT", 8080))
        store_url = f"http://{store_host}:{store_port}"

        response = _requests.post(f"{store_url}/api/stock-item", json=request_data)
