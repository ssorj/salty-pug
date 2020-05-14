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

from .client import *
from .model import *

from flask import Flask, Response, request, jsonify
from urllib.parse import quote_plus as url_escape

import os
import traceback as _traceback

def create_app(module_name, id):
    app = Flask(module_name)

    app.logger.setLevel(logging.INFO)

    configure_logging()

    # Defeat caching during development
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

    def handle_error(e):
        _traceback.print_exc()

        app.logger.error(e)

        return Response(f"Trouble! {e}\n\n{_traceback.format_exc()}", status=500, mimetype="text/plain")

    app.register_error_handler(Exception, handle_error)

    return app, Model(), Client()

def configure_logging():
    formatter = logging.Formatter("%(asctime)s %(levelname)-4.4s %(message)s")
    handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    for module in "client", "model":
        logger = logging.getLogger(module)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

def check_error(response):
    if response["error"] is not None:
        raise Exception(response["error"])

def generate_data():
    import random

    configure_logging()

    model = Model()
    client = Client()

    for i in range(20):
        store = random.choice(list(model._stores_by_id.values()))
        product = random.choice(list(model._products_by_id.values()))
        size = random.choice(model.sizes)
        color = random.choice(model.colors)

        order = Order(model, product, size, color, store=store)

        try:
            client.order_item(order)
        except:
            _traceback.print_exc()
