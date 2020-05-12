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

host = os.environ.get("FACTORY_SERVICE_HOST", "0.0.0.0")
port = int(os.environ.get("FACTORY_SERVICE_PORT", 8080))

app = Flask(__name__)
model = Model()

setup_app(app)

@app.route("/api/make-item", methods=["POST"])
def make_item():
    item = ProductItem.load(model, request.json["item"])
    store = model.get_store(request.json["store_id"])

    item.stock(store)

    return jsonify({
        "error": None,
        "factory_id": factory_id,
        "item_id": item.id,
    })

if __name__ == "__main__":
    app.run(host=host, port=port)
