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

store_id = os.environ.get("STORE_SERVICE_STORE_ID")
host = os.environ.get("STORE_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("STORE_SERVICE_PORT", 8080))

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

        with lock:
            items_by_id[self.id] = self

    def data(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "size": self.size,
            "color": self.color,
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id},{self.kind},{self.size},{self.color})"

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

@app.route("/api/stock-item", methods=["POST"])
def stock_item():
    item_data = request.json["item"]
    item = ProductItem(item_data["kind"], item_data["size"], item_data["color"], id=item_data["id"])

    return jsonify({
        "error": None,
    })

if __name__ == "__main__":
    app.run(host=host, port=port)
