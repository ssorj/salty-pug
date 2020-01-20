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

from flask import Flask, Response
from threading import Lock

app = Flask(__name__)

store_id = os.environ.get("STORE_SERVICE_STORE_ID")
host = os.environ.get("STORE_SERVICE_HOST", "localhost")
port = int(os.environ.get("STORE_SERVICE_PORT", 8080))

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/api/find-item")
def find_item():
    pass
    # return Response(f"Hello!", mimetype="text/plain")
    # return Response(f"Not found!", status=404, mimetype="text/plain")

@app.route("/api/hold-item")
def hold_item():
    pass

@app.route("/api/stock-item")
def stock_item():
    pass

if __name__ == "__main__":
    app.run(host=host, port=port)
