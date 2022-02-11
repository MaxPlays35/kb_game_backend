from typing import List
from .player import Player


class Game:
    def __init__(self, id, months=None) -> None:
        self.players: List[Player] = []
        self.id = id

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)
