from time import time

from flask import Flask, jsonify
from flask_socketio import SocketIO
import jwt

from routes.game import GameNamespace
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"

games = []


@app.get("/assets/<imageKey>")
def getImage():
    pass


@app.post("/login")
def login():
    return jwt.encode(
        {"nickname": "test", "profileImage": "braytech.png", "winrate": 50, "level": 1},
        app.config["SECRET_KEY"],
    )


socketio = SocketIO(app, cors_allowed_origins="*")

try:
    if __name__ == "__main__":
        socketio.on_namespace(GameNamespace("/game"))
        socketio.run(app)
except KeyboardInterrupt:
    exit(0)
