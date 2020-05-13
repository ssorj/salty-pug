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

from common import *

store_id = os.environ.get("STORE_SERVICE_STORE_ID")

app, model, client = create_app(__name__, store_id)

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
    item.store = model.get_store(store_id)

    model.add_item(item)

    return jsonify({
        "error": None,
    })

if __name__ == "__main__":
    host = os.environ.get("STORE_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("STORE_SERVICE_PORT", 8080))

    app.run(host=host, port=port)
