class Player:
    def __init__(
        self, nickname: str, profilePhoto: str, winrate: float, level: int, id: str
    ) -> None:
        self.__nickname = nickname
        self.__profilePhoto = profilePhoto
        self.__winrate = winrate
        self.__level = level
        self.__id = id
        self.__isReady = False
        self.__manufactories = 2
        self.__thousands = 10000
        self.__raw_materials = 4
        self.__destroyer = 2
        self.__missed_payments = 0

    def change_ready(self, value: bool) -> bool:
        self.__isReady = value
        return value

    @property
    def id(self):
        return self.__id

    @property
    def isReady(self):
        return self.__isReady

    def to_dict(
        self,
    ) -> dict[
        "nickname":str, "profilePhoto":str, "winrate":float, "level":int, "id":str
    ]:
        return {
            "nickname": self.__nickname,
            "profilePhoto": self.__profilePhoto,
            "winrate": self.__winrate,
            "level": self.__level,
            "id": self.__id,
            "isReady": self.__isReady,
        }
