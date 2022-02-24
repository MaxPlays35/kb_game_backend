from typing import Dict

from models.bank import Bank
from models.levels import level

from .offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from .player import Player


class Game:
    def __init__(self, id, months=None) -> None:
        self.players: Dict[str, Player] = {}
        self.id = id
        self.readyPlayers = 0
        self.__bank = Bank()
        self.__level = 3
        self.__current_month = 1
        self.players_ended_move = 0

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
        return self.__bank.proceed_produce_offer(offer, self.players[offer.player_id])

    def add_buy_offer(self, offer: BuyOffer):
        self.__bank.add_buy_offer(offer)

    def add_build_offer(self, offer: BuildOffer):
        return self.__bank.add_build_offer(
            offer, self.players[offer.player_id], self.__current_month
        )

    def add_auction_offer(self, offer: AuctionOffer):
        self.__bank.add_auction_offer(offer)

    def proceed_month(self):
        kicked_players = []
        current_state = level(
            sum([int(i.isAlive) for i in self.players.values()]), self.__level
        )
        self.__bank.proceed_buy_offers(current_state, self.players)
        if self.__current_month != 1:
            for player in self.players:
                self.__bank.withdraw_money(player)

    def get_state(self):
        alive_players = sum([int(i.isAlive) for i in self.players.values()])

        return level(alive_players, self.__level)
