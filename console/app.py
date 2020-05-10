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
import pprint
import random
import requests
import threading
import time

from flask import Flask, Response, request, jsonify, render_template

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

host = os.environ.get("CONSOLE_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("CONSOLE_SERVICE_PORT", 8080))

store_host_all = os.environ["STORE_SERVICE_HOST_ALL"]
store_port_all = int(os.environ.get("STORE_SERVICE_PORT_ALL", 8080))
store_all_url = f"http://{store_host_all}:{store_port_all}"

factory_host_any = os.environ["FACTORY_SERVICE_HOST_ANY"]
factory_port_any = int(os.environ.get("FACTORY_SERVICE_PORT_ANY", 8080))
factory_url_any = f"http://{factory_host_any}:{factory_port_any}"

def check_error(response_data):
    if response_data["error"] is not None:
        raise Exception(response_data["error"])

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/index.html")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/make-item", methods=["POST"])
def make_item():
    kind = request.form["kind"]
    size = request.form["size"]
    color = request.form["color"]

    request_data, response_data = _make_item(kind, size, color)

    check_error(response_data)

    request_data = pprint.pformat(request_data)
    response_data = pprint.pformat(response_data)

    return render_template("result.html",
                           request_data=request_data,
                           response_data=response_data)

def _make_item(kind, size, color):
    app.logger.info(f"Making item ({kind}, {size}, {color})")

    request_data = {"item": {"kind": kind, "size": size, "color": color}}
    response_data = requests.post(f"{factory_url_any}/api/make-item", json=request_data).json()

    return request_data, response_data

kinds = "cutlass", "parrot", "pegleg"
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

                _make_item(random.choice(kinds), random.choice(sizes), random.choice(colors))

make_item_thread = MakeItemThread()

if __name__ == "__main__":
    make_item_thread.run()

    app.run(host=host, port=port)
