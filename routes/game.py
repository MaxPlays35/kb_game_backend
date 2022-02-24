from flask_socketio import Namespace, emit, join_room
from flask import request
import jwt
import shortuuid

from models.game import Game
from models.message import Message
from models.offers import ProduceOffer
from models.player import Player

rooms: dict[str, Game] = {}
players: dict[str, Player] = {}


class GameNamespace(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)

    def on_connect(self):
        print("Client connected")

    # def on_message(self, data):
    #     temp = jwt.decode(data, "SECRET_KEY", "HS256")
    #     print(temp)
    #     print(data)

    def on_auth(self, jwt_token):
        identity = jwt.decode(jwt_token, "SECRET_KEY", "HS256")
        player = Player(
            identity["nickname"],
            identity["profilePhoto"],
            identity["winrate"],
            identity["level"],
            identity["id"],
            request.sid,
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
                for (_, player) in room.players.items():
                    players_local.append(player.to_dict())
                emit("users_list", players_local)
            room.add_player(data["id"], players[data["id"]])
        else:
            emit("error", {"error": "This room does not exist!"})

    def on_create_room(self, data):
        roomId = shortuuid.ShortUUID().random(length=10)
        game = Game(roomId)
        game.add_player(data["id"], players[data["id"]])
        rooms[roomId] = game
        emit("room_id", roomId)
        join_room(roomId)

    def on_ready_player(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.player_ready(data["id"], data["isReady"])
                emit(
                    "readiness_player",
                    {"id": player.id, "isReady": player.isReady},
                    include_self=False,
                    to=data["roomId"],
                )
            if room.readyPlayers == len(room.players) and len(room.players) > 1:
                emit(
                    "game_state", room.get_state(), to=data["roomId"], include_self=True
                )
                for player in room.players:
                    emit("p")
                emit("all_ready", to=data["roomId"], include_self=True)

    def on_leave_room(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.remove_player(data["id"])
                emit(
                    "player_leaved",
                    {"id": data["id"]},
                    include_self=False,
                    to=data["roomId"],
                )

    def on_player_auction(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.add_auction_offer(data["offer"])

    def on_player_buy(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.add_buy_offer(data["offer"])

    def on_player_build(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.add_build_offer(data["offer"])

    def on_player_produce(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["id"], False)
            if player:
                room.add_produce_offer(data["offer"])

    def on_message_server(self, data):
        emit(
            "message_client",
            Message(
                author=data["author"], message=data["message"], peerId=data["peerId"]
            ).to_json(),
            include_self=True,
            to=data["peerId"],
        )

    def on_produce_offer(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = players.get(data["playerId"], False)
            if player:
                room.add_produce_offer(
                    ProduceOffer(data["playerId"], data["destroyers"])
                )
