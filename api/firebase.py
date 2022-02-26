import requests
import hashlib
import shortuuid
import random

from models.player import Player


class FireBase:
    def __init__(self) -> None:
        self.base_usr = "https://kb-pum-default-rtdb.firebaseio.com/"

    def login_user(self, login: str, password: str):
        response = requests.get(self.base_usr + f"/players/{login}.json").json()
        if not response:
            return {
                "error": "Error",
                "user": None,
                "text": "Wrong login or password!",
                "success": False,
            }

        if response["password"] != hashlib.sha512(password.encode("utf-8")).hexdigest():
            return {
                "error": "Error",
                "user": None,
                "text": "Wrong login or password!",
                "success": False,
            }

        return {"error": "", "user": response, "success": True, "text": ""}

    def register_user(self, login: str, password: str):
        if requests.get(self.base_usr + f"/players/{login}.json").json() is not None:
            return {
                "error": "Error",
                "user": None,
                "text": "This user already exist!",
                "success": False,
            }

        response = requests.put(
            self.base_usr + f"/players/{login}.json",
            json={
                "nickname": login,
                "profilePhoto": "braytech.png",
                "level": 0,
                "id": shortuuid.ShortUUID().random(length=20),
                "wins": 0,
                "games": 0,
                "password": hashlib.sha512(password.encode("utf-8")).hexdigest(),
                "winrate": 0,
            },
        )

        return self.login_user(login, password)

    def increase_games(self, player: Player):
        old_value = requests.get(
            self.base_usr + f"/players/{player.nickname}/games.json"
        ).json()

        requests.patch(
            self.base_usr + f"/players/{player.nickname}/games.json", json=old_value + 1
        )

    def increase_wins(self, player: Player):
        old_value = requests.get(
            self.base_usr + f"/players/{player.nickname}/wins.json"
        ).json()

        requests.patch(
            self.base_usr + f"/players/{player.nickname}/wins.json", json=old_value + 1
        )

    def update_player(self, player: Player):
        pass
