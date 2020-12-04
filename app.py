from flask import Flask
from flask import request

import json

# curl localhost:5000/process?foo=value&bar=2

app = Flask(__name__)


@app.route("/process")
def my_api():
    params = dict(request.args)
    return {
        "username": "me",
        "theme": "me",
        "image": "me",
    }
