from operator import le
import random
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import jwt
import shortuuid

from routes.game import GameNamespace
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
CORS(app)

games = []


@app.get("/assets/<imageKey>")
def getImage():
    pass


@app.post("/login")
def login():
    player = {
        "nickname": shortuuid.ShortUUID().random(length=15),
        "profilePhoto": "braytech.png",
        "winrate": random.randint(0, 100),
        "level": random.randint(1, 10),
        "id": shortuuid.ShortUUID().random(length=20),
    }

    return jsonify(
        player=player,
        token=jwt.encode(
            player,
            app.config["SECRET_KEY"],
        ),
    )


socketio = SocketIO(app, cors_allowed_origins="*")

try:
    if __name__ == "__main__":
        socketio.on_namespace(GameNamespace("/game"))
        socketio.run(app, "0.0.0.0", 5000)
except KeyboardInterrupt:
    exit(0)
