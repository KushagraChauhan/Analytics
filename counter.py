'''page view counter in flask'''
from flask import Flask, jsonify
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

@app.route('/')
def index():
    with counter.get_lock():
        counter.value += 1

    return jsonify(count=counter.value)

app.run()
