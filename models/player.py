import json


class Player:
    def __init__(
        self, nickname: str, profilePhoto: str, winrate: float, level: int, id: str
    ) -> None:
        self.nickname = nickname
        self.profilePhoto = profilePhoto
        self.winrate = winrate
        self.level = level
        self.id = id
        self.manufactories = 2
        self.thousands = 10000
        self.raw_materials = 4
        self.destroyer = 2

    def __str__(self) -> str:
        return json.dumps(
            {
                "nickname": self.nickname,
                "profilePhoto": self.profilePhoto,
                "winrate": self.winrate,
                "level": self.level,
                "id": self.id,
            }
        )
