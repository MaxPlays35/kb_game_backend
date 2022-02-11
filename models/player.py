import json
from turtle import st


class Player:
    def __init__(
        self, nickname: str, profilePhoto: str, winrate: float, level: int, id: str
    ) -> None:
        self.nickname = nickname
        self.profilePhoto = profilePhoto
        self.winrate = winrate
        self.level = level
        self.id = id
        self.isReady = False
        self.manufactories = 2
        self.thousands = 10000
        self.raw_materials = 4
        self.destroyer = 2

    def change_ready(self, value: bool):
        self.isReady = value

    def to_dict(
        self,
    ) -> dict[
        "nickname":str, "profilePhoto":str, "winrate":float, "level":int, "id":str
    ]:
        return {
            "nickname": self.nickname,
            "profilePhoto": self.profilePhoto,
            "winrate": self.winrate,
            "level": self.level,
            "id": self.id,
            "isReady": self.isReady,
        }
