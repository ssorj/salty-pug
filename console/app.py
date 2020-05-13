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
    out.append("<tr><th>ID</th><th>Kind</th><th>Size</th><th>Color</th><th>Store</th></tr>");

    items = client.find_items(None, None, None)

    for item in items:
        out.append("<tr>");
        out.append(f"<td>{item['id']}</td>");
        out.append(f"<td>{item['product_id']}</td>");
        out.append(f"<td>{item['size']}</td>");
        out.append(f"<td>{item['color']}</td>");
        out.append(f"<td>{item.get('store_id')}</td>");
        out.append("</tr>");

    out.append("</table>");

    return Markup("".join(out))

def inventory_data_link():
    url = url_escape(client.find_items_url(None, None, None))
    return Markup(f"<a href='/pretty-data?url={url}'>Data</a>")

@app.route("/orders/index.html")
@app.route("/orders/")
def orders_index():
    return render_template("/orders/index.html")

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

# @app.route("/make-item", methods=["POST"])
# def make_item():
#     kind = request.form["kind"]
#     size = request.form["size"]
#     color = request.form["color"]

#     request_data, response_data = _make_item(kind, size, color)

#     check_error(response_data)

#     request_data = pprint.pformat(request_data)
#     response_data = pprint.pformat(response_data)

#     return render_template("result.html",
#                            request_data=request_data,
#                            response_data=response_data)

if __name__ == "__main__":
    host = os.environ.get("CONSOLE_SERVICE_HOST", "0.0.0.0")
    port = int(os.environ.get("CONSOLE_SERVICE_PORT", 8080))

    app.run(host=host, port=port)
