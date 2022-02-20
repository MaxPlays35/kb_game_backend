from typing import Any, Dict

from models.bank import Bank

from .offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from .player import Player


class Game:
    def __init__(self, id, months=None) -> None:
        self.players: Dict[str, Player] = {}
        self.id = id
        self.readyPlayers = 0
        self.__bank = Bank()

    def add_player(self, id: str, player: Player):
        self.players.update({id: player})

    def remove_player(self, id):
        del self.players[id]

    def player_ready(self, id: str, value: bool):
        if self.players[id].change_ready(value):
            self.readyPlayers += 1
        else:
            self.readyPlayers -= 1

    def add_produce_offer(self, offer: ProduceOffer):
        self.__bank.add_produce_offer(offer)

    def add_buy_offer(self, offer: BuyOffer):
        self.__bank.add_buy_offer(offer)

    def add_build_offer(self, offer: BuildOffer):
        self.__bank.add_build_offer(offer)

    def add_auction_offer(self, offer: AuctionOffer):
        self.__bank.add_auction_offer(offer)
