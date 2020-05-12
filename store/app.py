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

from flask import Flask, Response, request, jsonify
from model import *

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

store_id = os.environ.get("STORE_SERVICE_STORE_ID")

host = os.environ.get("STORE_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("STORE_SERVICE_PORT", 8080))

model = Model()

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/api/find-items")
def find_items():
    product = model.get_product(request.args.get("product_id"))
    size = request.args.get("size")
    color = request.args.get("color")

    results = model.find_items(product, size, color)

    return jsonify({
        "error": None,
        "items": results,
    })

@app.route("/api/stock-item", methods=["POST"])
def stock_item():
    item = ProductItem.load(model, request.json["item"])

    model.add_item(item)

    return jsonify({
        "error": None,
    })

if __name__ == "__main__":
    app.run(host=host, port=port)
