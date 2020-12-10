from flask import Flask
from flask import request
from flask_cors import CORS

import json
import time

from processing import Processor

# curl localhost:5000/process?foo=value&bar=2

app = Flask(__name__)
CORS(app)

# TODO write validators


@app.route("/process")
def my_api():
    # print
    params = dict(request.args)
    start = time.time()
    dict_data = Processor(params).process()
    print(time.time() - start)
    json_to_send = json.dumps(dict_data)

    return json_to_send
