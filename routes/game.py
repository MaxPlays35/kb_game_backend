from flask_socketio import Namespace, emit, join_room, leave_room
from flask import request
import jwt
import shortuuid

from models.game import Game
from models.message import Message
from models.offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from models.player import Player
import api.firebase

firebase = api.firebase.FireBase()


rooms: dict[str, Game] = {}
players: dict[str, Player] = {}


def cap(player: Player, current_state):
    pend = sum([i["workshops"] for i in player.pending_manufactories])
    score = 0
    score += player.manufactories * 5000
    score += pend * 5000
    score += player.raw_materials * current_state["minPriceRaw"]
    score += player.destroyers * current_state["maxPriceDestroyer"]
    score += player.money
    score -= pend * 2500

    return score


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
                "finish_connect",
                data["roomId"],
                to=players[data["id"]].peer_id,
                include_self=True,
            )
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
            emit("error", {"text": "This room does not exist!", "error": "Error "})

    def on_create_room(self, data):
        roomId = shortuuid.ShortUUID().random(length=10)
        game = Game(roomId, data["months"])
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
                for player in room.players.values():
                    print(player.get_state())
                    emit("user_state", player.get_state(), to=player.id)
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
                leave_room(data["roomId"])

    def on_auction_offer(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["playerId"], False)
            if player:
                result = room.add_auction_offer(
                    AuctionOffer(
                        player_id=data["playerId"],
                        aircrafts=data["destroyers"],
                        price=data["price"],
                    )
                )
                if not result["success"]:
                    emit("error", {"text": result["text"], "error": "Error"})

    def on_buy_offer(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["playerId"], False)
            if player:
                result = room.add_buy_offer(
                    BuyOffer(
                        player_id=data["playerId"],
                        raw_material=data["rawMaterials"],
                        price=data["price"],
                    )
                )

                if not result["success"]:
                    emit("error", {"text": result["text"]})

    def on_build_offer(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["playerId"], False)
            if player:
                result = room.add_build_offer(
                    BuildOffer(
                        player_id=data["playerId"], workshops=data["manufactories"]
                    )
                )
                if not result["success"] and result["bankrupt"]:
                    emit("bankrupt", to=player.peer_id)
                    room.remove_player(data["playerId"])
                    emit(
                        "player_leaved",
                        {"id": data["playerId"]},
                        include_self=False,
                        to=data["roomId"],
                    )
                    leave_room(data["roomId"])
                    return
                elif not result["success"]:
                    emit("error", {"text": result["text"]})
                    return

                emit("user_state", player.get_state(), to=player.peer_id)

    def on_produce_offer(self, data):
        room = rooms.get(data["roomId"], False)
        print(data)
        if room:
            player = room.players.get(data["playerId"], False)
            if player:
                result = room.add_produce_offer(
                    ProduceOffer(
                        player_id=data["playerId"], aircrafts=data["destroyers"]
                    )
                )
                if not result["success"]:
                    emit("error", {"text": result["text"], "error": "Error"})
                    return

                emit("user_state", player.get_state(), to=player.peer_id)

    def on_message_server(self, data):
        emit(
            "message_client",
            Message(
                author=data["author"], message=data["message"], peerId=data["peerId"]
            ).to_json(),
            include_self=True,
            to=data["peerId"],
        )

    def on_disconnect_user(self, data):
        print(data)

    def on_end_move(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            player = room.players.get(data["playerId"], False)
            if player:
                if data["playerId"] in room.players_ended_move:
                    emit(
                        "error",
                        {"error": "Error", "text": "You have already ended move"},
                    )
                else:
                    room.players_ended_move.add(data["playerId"])
                if len(room.players_ended_move) == len(room.players):
                    result = room.proceed_month()
                    for player in result["kicked_players"]:
                        emit("bankrupt", to=result["kicked_players"][player].peer_id)
                        room.remove_player(player)
                        players[player].clean()
                        emit(
                            "player_leaved",
                            {"id": data["playerId"]},
                            include_self=False,
                            to=data["roomId"],
                        )
                        leave_room(
                            data["roomId"], sid=result["kicked_players"][player].peer_id
                        )
                    if result["end"]:
                        players_local = list(room.players.values())
                        win_player = sorted(
                            players_local,
                            key=lambda item: cap(item, room.get_state()),
                            reverse=True,
                        )[0]
                        emit(
                            "win",
                            {"error": "Victory", "text": "You win!"},
                            to=win_player.peer_id,
                        )
                        players_local.remove(win_player)
                        room.remove_player(win_player.id)
                        leave_room(data["roomId"], sid=win_player.peer_id)
                        win_player.clean()
                        for player in list(room.players.values()):
                            emit(
                                "win",
                                {"error": "Survived", "text": "You survived!"},
                                to=player.peer_id,
                            )
                            room.remove_player(player.id)
                            leave_room(data["roomId"], sid=player.peer_id)
                            players[player.id].clean()
                        return

                    if len(room.players) == 1:
                        player = list(room.players.values())[0]
                        emit(
                            "win",
                            {"error": "Victory", "text": "You win!"},
                            to=player.peer_id,
                        )
                        players[player.id].clean()

                    else:
                        emit("game_state", room.get_state(), to=data["roomId"])
                        for player in room.players.values():
                            emit("user_state", player.get_state(), to=player.peer_id)
