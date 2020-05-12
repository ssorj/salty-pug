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

import binascii as _binascii
import requests as _requests
import threading as _threading
import uuid as _uuid

# XXX

store_host_all = os.environ["STORE_SERVICE_HOST_ALL"]
store_port_all = int(os.environ.get("STORE_SERVICE_PORT_ALL", 8080))
store_all = f"http://{store_host_all}:{store_port_all}"

class Model:
    def __init__(self):
        self._lock = _threading.Lock()

        self._stores_by_id = dict()
        self._factories_by_id = dict()
        self._products_by_id = dict()
        self._items_by_id = dict()

        self.store_1 = Store(self, "Store 1", id="store-1")
        self.store_2 = Store(self, "Store 2", id="store-2")
        self.store_3 = Store(self, "Store 3", id="store-3")

        self.factory_1 = Factory(self, "Factory 1", id="factory-1")
        self.factory_2 = Factory(self, "Factory 2", id="factory-2")
        self.factory_3 = Factory(self, "Factory 3", id="factory-3")

        self.cutlass = Product(self, "Cutlass", id="cutlass")
        self.parrot = Product(self, "Parrot", id="parrot")
        self.pegleg = Product(self, "Pegleg", id="pegleg")

        self.sizes = "small", "medium", "large"
        self.colors = "red", "green", "blue"

    def get_store(self, store_id):
        with self._lock:
            return self._stores_by_id.get(store_id)

    def get_factory(self, factory_id):
        with self._lock:
            return self._factories_by_id.get(factory_id)

    def get_product(self, product_id):
        with self._lock:
            return self._products_by_id.get(product_id)

    def get_item(self, item_id):
        with self._lock:
            return self._items_by_id.get(item_id)

    def add_item(self, item):
        with self._lock:
            self._items_by_id[item.id] = item

    def find_items(self, product, size, color):
        results = list()

        with self._lock:
            for item in self._items_by_id.values():
                if product is None or item.product is product:
                    if size is None or item.size == size:
                        if color is None or item.color == color:
                            results.append(item.data())

        return results

    def find_items_all_stores(self, product, size, color):
        data = _requests.get(f"{store_all}/api/find-items").json()

        # Special case for non-aggregated result used in testing
        if isinstance(data, dict):
            data = [data]

        results = list()

        # XXX Check for errors

        for response in data:
            results.extend(response["content"]["items"])

        return results, data

class Store:
    def __init__(self, model, name, id=None):
        self.model = model
        self.name = name
        self.id = id

        if self.id is None:
            self.id = _unique_id()

        with self.model._lock:
            self.model._stores_by_id[self.id] = self

class Factory:
    def __init__(self, model, name, id=None):
        self.model = model
        self.name = name
        self.id = id

        if self.id is None:
            self.id = _unique_id()

        with self.model._lock:
            self.model._factories_by_id[self.id] = self

class Product:
    def __init__(self, model, name, id=None):
        self.model = model
        self.name = name
        self.id = id

        if self.id is None:
            self.id = _unique_id()

        with self.model._lock:
            self.model._products_by_id[self.id] = self

class ProductItem:
    def __init__(self, model, product, size, color, id=None):
        assert product is not None
        assert size in ("small", "medium", "large")
        assert color in ("red", "green", "blue")

        self.id = id
        self.model = model
        self.product = product
        self.size = size
        self.color = color
        self.store = None

        if self.id is None:
            self.id = _unique_id()

        with self.model._lock:
            self.model._items_by_id[self.id] = self

    @staticmethod
    def load(model, data):
        product = model.get_product(data["product_id"])
        return ProductItem(model, product, data["size"], data["color"], id=data.get("id"))

    def data(self):
        return {
            "id": self.id,
            "product_id": self.product.id,
            "size": self.size,
            "color": self.color,
            "store_id": (None if self.store is None else self.store.id),
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id},{self.product.id},{self.size},{self.color})"

    # Store calls factory
    def make(self, store):
        factory_host = os.environ["FACTORY_SERVICE_HOST_ANY"]
        factory_port = int(os.environ.get("FACTORY_SERVICE_PORT_ANY", 8080))

        request_data = {
            "item": self.data(),
            "store_id": store.id,
        }

        response = _requests.post(f"http://{factory_host}:{factory_port}/api/make-item", json=request_data)

    # Factory calls store
    def stock(self, store):
        request_data = {
            "item": self.data(),
        }

        store_host = os.environ.get("STORE_SERVICE_HOST_OVERRIDE", store.id)
        store_port = int(os.environ.get("STORE_SERVICE_PORT", 8080))

        response = _requests.post(f"http://{store_host}:{store_port}/api/stock-item", json=request_data)

def _unique_id():
    uuid_bytes = _uuid.uuid4().bytes
    uuid_bytes = uuid_bytes[:4]

    return _binascii.hexlify(uuid_bytes).decode("utf-8")
