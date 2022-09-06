from flask import Flask, request
from threading import Thread
import logging

app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True


@app.route("/", methods=["POST"])
def receive():
    data = request.json
    if not data:
        return "Bad event", 400
    if (data["post_type"] == "meta_event" and
            data["meta_event_type"] == "heartbeat"):
        return "OK", 200
    print(data)
    return "OK", 200


def start(port: int):
    global thrd
    thrd = Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": port}, daemon=True
    )
    thrd.start()