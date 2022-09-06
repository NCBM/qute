from flask import Flask, request
from threading import Thread
import logging

from qute.utils import topprint
from qute.core import friend_msg_queue, group_msg_queue

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
    topprint(data, sep="")
    if data["post_type"] == "message":
        if data["message_type"] == "group":
            group_msg_queue[data["group_id"]].append(data["message_id"])
        elif data["message_type"] == "friend":
            friend_msg_queue[data["user_id"]].append(data["message_id"])
    return "OK", 200


def start(port: int):
    global thrd
    thrd = Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": port}, daemon=True
    )
    thrd.start()