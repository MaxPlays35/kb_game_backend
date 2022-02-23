from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    author: dict[str, str]
    message: str
    peerId: str
    time: str = str(datetime.now())

    def to_json(self):
        return {
            "author": {
                "nickname": self.author["nickname"],
                "profilePhoto": self.author["profilePhoto"],
            },
            "message": self.message,
            "time": self.time,
            "peerId": self.peerId,
        }
