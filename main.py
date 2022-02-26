import random
from flask import Flask, jsonify, request, make_response
from flask_socketio import SocketIO
from flask_cors import CORS
import jwt
import shortuuid
import api.firebase

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
    data = request.json
    result = api.firebase.FireBase().login_user(
        login=data["login"], password=data["password"]
    )

    if not result["success"]:
        return jsonify(result), 200

    return (
        jsonify(
            player=result["user"],
            token=jwt.encode(
                result["user"],
                app.config["SECRET_KEY"],
            ),
            error=result["error"],
            success=result["success"],
            text=result["text"],
        ),
        200,
    )


@app.post("/register")
def register():
    data = request.json
    result = api.firebase.FireBase().register_user(
        login=data["login"], password=data["password"]
    )

    if not result["success"]:
        return jsonify(result), 200

    return (
        jsonify(
            player=result["user"],
            token=jwt.encode(
                result["user"],
                app.config["SECRET_KEY"],
            ),
            error=result["error"],
            success=result["success"],
            text=result["text"],
        ),
        200,
    )


socketio = SocketIO(app, cors_allowed_origins="*")

try:
    if __name__ == "__main__":
        socketio.on_namespace(GameNamespace("/game"))
        socketio.run(app, "0.0.0.0", 10000)
except KeyboardInterrupt:
    exit(0)
