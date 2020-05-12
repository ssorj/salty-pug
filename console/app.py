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

import requests
import threading

host = os.environ.get("CONSOLE_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("CONSOLE_SERVICE_PORT", 8080))

store_host_all = os.environ["STORE_SERVICE_HOST_ALL"]
store_port_all = int(os.environ.get("STORE_SERVICE_PORT_ALL", 8080))
store_all = f"http://{store_host_all}:{store_port_all}"

factory_host_any = os.environ["FACTORY_SERVICE_HOST_ANY"]
factory_port_any = int(os.environ.get("FACTORY_SERVICE_PORT_ANY", 8080))
factory_any = f"http://{factory_host_any}:{factory_port_any}"

app = Flask(__name__)
model = Model()

setup_app(app)

@app.route("/index.html")
@app.route("/")
def index():
    return render_template("index.html", func=func)

def func():
    return "Hello"

@app.route("/inventory/index.html")
@app.route("/inventory/")
def inventory_index():
    return render_template("/inventory/index.html", inventory_table=inventory_table)

def inventory_table():
    out = list()

    response_data = requests.get(f"{store_all}/api/find-items").json()
    items = response_data["items"]

    out.append(f"<pre>{response_data}</pre>");

    out.append("<table>");
    out.append("<tr><th>ID</th><th>Kind</th><th>Size</th><th>Color</th></tr>");

    for item in items:
        out.append("<tr>");
        out.append(f"<td>{item['id']}</td>");
        out.append(f"<td>{item['kind']}</td>");
        out.append(f"<td>{item['size']}</td>");
        out.append(f"<td>{item['color']}</td>");
        out.append("</tr>");

    out.append("</table>");

    return Markup("".join(out))

@app.route("/orders/index.html")
@app.route("/ordres/")
def orders_index():
    return render_template("/orders/index.html", func=func)

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

# def _make_item(kind, size, color):
#     app.logger.info(f"Making item ({kind}, {size}, {color})")

#     request_data = {"item": {"kind": kind, "size": size, "color": color}}
#     response_data = requests.post(f"{factory_any}/api/make-item", json=request_data).json()

#     return request_data, response_data

sizes = "small", "medium", "large"
colors = "red", "green", "blue"

class MakeItemThread(threading.Thread):
    def __init__(self):
        super().__init__()

        self.daemon = True
        self.enabled = True

    def run(self):
        while True:
            time.sleep(1)

            while self.enabled:
                time.sleep(1)

                with model._lock:
                    store = random.choice(list(model._stores_by_id.values()))
                    product = random.choice(list(model._products_by_id.values()))

                size = random.choice(sizes)
                color = random.choice(colors)

                item = ProductItem(model, product, size, color)

                print(111)
                item.make(store)

make_item_thread = MakeItemThread()

if __name__ == "__main__":
    make_item_thread.start()

    app.run(host=host, port=port, debug=True)
