from flask import Flask
from threading import Thread

app = Flask(__name__)

thrd = Thread(target=app.run)

thrd.start()