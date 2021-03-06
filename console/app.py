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

from flask import Markup, render_template

app, model, client = create_app(__name__, "console")

@app.route("/index.html")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inventory/index.html")
@app.route("/inventory/")
def inventory_index():
    return render_template("/inventory/index.html", inventory_table=inventory_table, inventory_data_link=inventory_data_link)

def inventory_table():
    out = list()

    out.append("<table>");
    out.append("<tr><th>ID</th><th>Product</th><th>Size</th><th>Color</th><th>Store</th><th>Origin</th></tr>");

    results = client.find_items()

    for result in results:
        out.append("<tr>");
        out.append(f"<td>{result['id']}</td>");
        out.append(f"<td>{result['product_id']}</td>");
        out.append(f"<td>{result['size']}</td>");
        out.append(f"<td>{result['color']}</td>");
        out.append(f"<td>{result['store_id']}</td>");
        out.append(f"<td>{result['factory_id']}</td>");
        out.append("</tr>");

    out.append("</table>");

    return Markup("".join(out))

def inventory_data_link():
    url = url_escape(client.find_items_url())
    return Markup(f"<a href='/pretty-data?url={url}'>Data</a>")

@app.route("/orders/index.html")
@app.route("/orders/")
def orders_index():
    return render_template("/orders/index.html", orders_table=orders_table, orders_data_link=orders_data_link)

@app.route("/orders/create.html")
def orders_create():
    return render_template("/orders/create.html")

@app.route("/orders/create-result.html", methods=["POST"])
def orders_create_result():
    product = model.get_product(request.form["product_id"])
    store = model.get_store(request.form["store_id"])
    size = request.form["size"]
    color = request.form["color"]

    order = Order(model, product, store, size, color)

    request_data, response_data = client.order_item(order)

    import pprint
    request_data, response_data = pprint.pformat(request_data), pprint.pformat(response_data)

    return render_template("/orders/create-result.html", request_data=request_data, response_data=response_data)

def orders_table():
    out = list()

    out.append("<table>");
    out.append("<tr><th>ID</th><th>Status</th><th>Product</th><th>Size</th><th>Color</th><th>Factory</th><th>Destination</th></tr>");

    results = client.find_orders()

    for result in results:
        out.append("<tr>");
        out.append(f"<td>{result['id']}</td>");
        out.append(f"<td>{result['status']}</td>");
        out.append(f"<td>{result['product_id']}</td>");
        out.append(f"<td>{result['size']}</td>");
        out.append(f"<td>{result['color']}</td>");
        out.append(f"<td>{result['factory_id']}</td>");
        out.append(f"<td>{result['store_id']}</td>");
        out.append("</tr>");

    out.append("</table>");

    return Markup("".join(out))

def orders_data_link():
    url = url_escape(client.find_orders_url())
    return Markup(f"<a href='/pretty-data?url={url}'>Data</a>")

@app.route("/pretty-data")
def scripts_pretty_data():
    import pprint

    url = request.args["url"]
    data = client.get_json(url)
    pretty_data = pprint.pformat(data)

    return Response(pretty_data, status=200, mimetype="text/plain")

@app.route("/scripts/generate-data")
def scripts_generate_data():
    generate_data()
    return Response("OK\n", status=200, mimetype="text/plain")

@app.route("/favicon.ico")
def favicon():
    return Response("I blame Microsoft for this bullshit\n", status=200, mimetype="text/plain")

if __name__ == "__main__":
    host = os.environ.get("CONSOLE_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("CONSOLE_SERVICE_PORT", 8080))

    app.run(host=host, port=port, debug=True)
