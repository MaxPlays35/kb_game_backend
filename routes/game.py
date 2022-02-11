from copy import copy, deepcopy
from re import I
from flask_socketio import Namespace, emit, join_room, send
import jwt
import shortuuid

from models.game import Game
from models.player import Player

rooms: dict[str, Game] = {}
players: dict[str, Player] = {}


class GameNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)

    def on_connect(self):
        print("Client connected")

    def on_message(self, data):
        temp = jwt.decode(data, "SECRET_KEY", "HS256")
        print(temp)
        print(data)

    def on_auth(self, jwt_token):
        identity = jwt.decode(jwt_token, "SECRET_KEY", "HS256")
        player = Player(
            identity["nickname"],
            identity["profilePhoto"],
            identity["winrate"],
            identity["level"],
            identity["id"],
        )
        players[identity["id"]] = player
        emit("authed", player.to_dict())

    def on_join_room(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            join_room(data["roomId"])
            emit(
                "user_joined",
                players[data["id"]].to_dict(),
                to=data["roomId"],
                include_self=False,
            )
            if len(room.players):
                players_local = []
                for player in room.players:
                    players_local.append(player.to_dict())
                emit("users_list", players_local)
            room.add_player(players[data["id"]])
        else:
            emit("error", {"error": "This room does not exist!"})

    def on_create_room(self, data):
        roomId = shortuuid.ShortUUID().random(length=10)
        game = Game(roomId)
        game.add_player(players[data["id"]])
        rooms[roomId] = game
        emit("room_id", roomId)
        join_room(roomId)

    def on_ready_player(self, data):
        players[data["id"]].change_ready(data["isReady"])
        emit(
            "readiness_player",
            {"id": players[data["id"]].id, "isReady": players[data["id"]].isReady},
            include_self=False,
            to=data["roomId"],
        )

    def on_leave_room(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = players[data["id"]]
            room.remove_player(player)
            emit(
                "player_leaved",
                {"id": data["id"]},
                include_self=False,
                to=data["roomId"],
            )
