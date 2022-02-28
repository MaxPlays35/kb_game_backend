class Player:
    def __init__(
        self,
        nickname: str,
        profilePhoto: str,
        winrate: float,
        level: int,
        id: str,
        peer_id: str,
    ) -> None:
        self.nickname = nickname
        self.profilePhoto = profilePhoto
        self.winrate = winrate
        self.level = level
        self.id = id
        self.__peer_id = peer_id
        self.__isReady = False
        self.__manufactories = 2
        self.__thousands = 10000
        self.__raw_materials = 4
        self.__destroyers = 2
        self.__isAlive = True
        self.__pending_destroyers = 0
        self.pending_manufactories = []

    def change_ready(self, value: bool) -> bool:
        self.__isReady = value
        return value

    @property
    def isReady(self):
        return self.__isReady

    @property
    def peer_id(self):
        return self.__peer_id

    @property
    def raw_materials(self):
        return self.__raw_materials

    @property
    def destroyers(self):
        return self.__destroyers

    @property
    def manufactories(self):
        return self.__manufactories

    @property
    def isAlive(self):
        return self.__isAlive

    @property
    def money(self):
        return self.__thousands

    def get_state(self):
        return {
            "money": self.__thousands,
            "raw_materials": self.__raw_materials,
            "destroyers": self.__destroyers,
            "manufactories": self.__manufactories,
            "player_id": self.id,
        }

    def withdraw_money(self, money: int):
        if self.__thousands - money > 0:
            self.__thousands -= money
            return True

        return False

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
            "peerId": self.__peer_id,
            "isReady": self.__isReady,
            "isAlive": self.__isAlive,
        }

    def add_pending_destroyers(self, destroyers):
        self.__pending_destroyers += destroyers

    def add_destroyers(self):
        self.__destroyers += self.__pending_destroyers
        self.__pending_destroyers = 0

    def add_pending_manufactories(self, offer):
        self.__manufactories += offer["workshops"]

    def add_manufactories(self, data):
        self.pending_manufactories.append(data)

    def add_raw_materials(self, raw_materials: int):
        self.__raw_materials += raw_materials

    def add_money(self, money: int):
        self.__thousands += money

    def remove_destroyers(self, destroyers):
        self.__destroyers -= destroyers

    def remove_raw_materials(self, raw_materials):
        self.__raw_materials -= raw_materials

    def clean(self):
        self.__isReady = False
        self.__manufactories = 2
        self.__thousands = 10000
        self.__raw_materials = 4
        self.__destroyers = 2
        self.__isAlive = True
        self.__pending_destroyers = 0
        self.pending_manufactories = []
