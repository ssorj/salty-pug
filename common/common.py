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

from model import *

import random
import time

from flask import Flask, Response, Markup, request, jsonify, render_template

_app = None

def setup_app(app):
    global _app
    _app = app

    app.logger.setLevel(logging.INFO)

    # Defeat caching during development
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.register_error_handler(Exception, _handle_error)

def _handle_error(e):
    _app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

def check_error(response):
    if response["error"] is not None:
        raise Exception(response["error"])
