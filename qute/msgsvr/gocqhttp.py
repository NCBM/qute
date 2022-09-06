from flask import Flask
from threading import Thread

app = Flask(__name__)


def start(port: int):
    global thrd
    thrd = Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": port}, daemon=True
    )
    thrd.start()