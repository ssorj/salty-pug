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

import os
import requests
import uuid

from flask import Flask, Response, request, jsonify
from threading import Lock

app = Flask(__name__)

factory_id = os.environ.get("FACTORY_SERVICE_FACTORY_ID")
host = os.environ.get("FACTORY_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("FACTORY_SERVICE_PORT", 8080))

store_host_any = os.environ["STORE_SERVICE_HOST_ANY"]
store_port_any = int(os.environ.get("STORE_SERVICE_PORT_ANY", 8080))
store_any_base_url = f"http://{store_host_any}:{store_port_any}"

store_host_all = os.environ["STORE_SERVICE_HOST_ALL"]
store_port_all = int(os.environ.get("STORE_SERVICE_PORT_ALL", 8080))
store_all_base_url = f"http://{store_host_all}:{store_port_all}"

lock = Lock()
items_by_id = dict()

class ProductItem:
    def __init__(self, kind, size, color, id=None):
        assert kind in ("cutlass", "parrot", "pegleg")
        assert size in ("small", "medium", "large")
        assert color in ("red", "green", "blue")

        self.id = str(uuid.uuid4())
        self.kind = kind
        self.size = size
        self.color = color
        self.status = "making"

        with lock:
            items_by_id[self.id] = self

    def finish_making(self):
        self.status = "made"

    def data(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "size": self.size,
            "color": self.color,
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id},{self.kind},{self.size},{self.color},{self.status})"

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/api/find-items")
def find_items():
    kind = request.args["kind"]
    size = request.args.get("size")
    color = request.args.get("color")

    results = list()

    with lock:
        for item in items_by_id.values():
            if item.kind == kind:
                if size is None or item.size == size:
                    if color is None or item.color == color:
                        results.append(item.data())

    return jsonify({
        "error": None,
        "items": results,
    })

@app.route("/api/make-item", methods=["POST"])
def make_item():
    item_data = request.json["item"]
    item = ProductItem(item_data["kind"], item_data["size"], item_data["color"])

    item.finish_making() # XXX

    return jsonify({
        "error": None,
        "factory_id": factory_id,
        "item_id": item.id,
    })

@app.route("/api/check-item-status")
def check_item_status():
    item_id = request.args["id"]

    with lock:
        item = items_by_id[item_id]

    return jsonify({
        "error": None,
        "status": item.status,
    })

@app.route("/api/ship-item", methods=["POST"])
def ship_item():
    data = request.json
    item = items_by_id[data["item_id"]]
    store_id = data["store_id"]

    data = {
        "item": item.data(),
    }

    # XXX need to direct this to a particular store
    requests.post(f"{store_any_base_url}/api/stock-item", json=data)

    with lock:
        del items_by_id[item.id]

    return jsonify({
        "error": None,
    })

if __name__ == "__main__":
    app.run(host=host, port=port)
