from flask_socketio import Namespace, emit, join_room, send
import jwt
import shortuuid

from models.game import Game
from models.player import Player

rooms: dict[str, Game] = {}


class GameNamespace(Namespace):
    nickname: str
    profilePhoto: str
    winrate: float
    level: int

    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.nickname = ""
        self.profilePhoto = ""
        self.winrate = 0.0
        self.level = 0

    def on_connect(self):
        print("Client connected")

    def on_message(self, data):
        temp = jwt.decode(data, "SECRET_KEY", "HS256")
        print(temp)
        print(data)

    def on_auth(self, jwt_token):
        identity = jwt.decode(jwt_token, "SECRET_KEY", "HS256")
        self.player = Player(
            identity["nickname"],
            identity["profilePhoto"],
            identity["winrate"],
            identity["level"],
            shortuuid.ShortUUID().random(length=20),
        )

    def on_join_room(self, data):
        room = rooms.get(data["roomId"], False)
        if room:
            join_room(data["roomId"])
            room.add_player(self.player)
            emit(
                "user_joined",
                {
                    "nickname": self.player.nickname,
                    "profilePhoto": self.player.profilePhoto,
                    "winrate": self.player.winrate,
                    "level": self.player.level,
                },
                to=data["roomId"],
                include_self=False,
            )
            if len(room.players):
                players = []
                for player in room.players:
                    players.append(str(player))
                emit("users_list", players)
        else:
            emit("error", {"error": "This room does not exist!"})

    def on_create_room(self):
        roomId = shortuuid.ShortUUID().random(length=10)
        game = Game(roomId)
        game.add_player(self.player)
        rooms[roomId] = game
        emit("room_id", roomId)
        join_room(roomId)
