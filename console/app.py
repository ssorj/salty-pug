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
import requests

from flask import Flask, Response, request, jsonify

app = Flask(__name__)

host = os.environ.get("CONSOLE_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("CONSOLE_SERVICE_PORT", 8080))

@app.errorhandler(Exception)
def error(e):
    app.logger.error(e)
    return Response(f"Trouble! {e}\n", status=500, mimetype="text/plain")

@app.route("/")
def index():
    return """
<html>
  <head>
    <title>Salty Pug console</title>
    <link rel="icon" href="data:;base64,iVBORw0KGgo="/>
  </head>
  <body>
    <h1>Salty Pug console</h1>

    <h2>Make item</h2>

    <form action="/make-item" method="post">
      <p>Kind</p>
      <p><input name="kind" value="cutlass"/></p>
      <p>Size</p>
      <p><input name="size" value="large"></p>
      <p>Color</p>
      <p><input name="color" value="blue"/></p>
      <p><button type="submit">Submit</button></p>
    </form>
  </body>
</html>
""".strip()

@app.route("/make-item", methods=["POST", "GET"])
def make_item():
    if request.method == "GET":
        return "YUP"

    print(222, request.method)

    kind = request.form["kind"]
    size = request.form["size"]
    color = request.form["color"]

    print(111, kind, size, color)

    return "OK"

if __name__ == "__main__":
    app.run(host=host, port=port)
