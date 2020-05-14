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

factory_id = os.environ.get("FACTORY_SERVICE_FACTORY_ID")

app, model, client = create_app(__name__, factory_id)

@app.route("/api/find-orders")
def find_orders():
    product = model.get_product(request.args.get("product_id"))
    size = request.args.get("size")
    color = request.args.get("color")

    results = model.find_orders(product, size, color)

    return jsonify({
        "error": None,
        "results": results,
    })

@app.route("/api/order-item", methods=["POST"])
def order_item():
    order = Order.load(model, request.json["order"])
    factory = model.get_factory(factory_id)

    order.factory = factory
    model.add_order(order)

    order.item = Item(model, order.product, order.store, order.factory, order.size, order.color)

    client.stock_item(order.item)

    order.status = "fulfilled"

    return jsonify({
        "error": None,
        "order": order.data(),
    })

if __name__ == "__main__":
    host = os.environ.get("FACTORY_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("FACTORY_SERVICE_PORT", 8080))

    app.run(host=host, port=port)
