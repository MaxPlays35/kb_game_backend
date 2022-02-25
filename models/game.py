from random import choices, random
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
        self.max_months = months if months else 9999

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
        return self.__bank.add_buy_offer(offer)

    def add_build_offer(self, offer: BuildOffer):
        return self.__bank.add_build_offer(
            offer, self.players[offer.player_id], self.__current_month
        )

    def add_auction_offer(self, offer: AuctionOffer):
        return self.__bank.add_auction_offer(offer)

    def proceed_month(self):
        self.players_ended_move = 0
        kicked_players = {}
        current_state = level(
            sum([int(i.isAlive) for i in self.players.values()]), self.__level
        )
        self.__bank.proceed_buy_offers(current_state, self.players)
        self.__bank.proceed_auction_offers(current_state, self.players)
        self.__current_month += 1
        if self.__current_month != 2:
            for player in self.players:
                if self.__bank.withdraw_money(player) == False:
                    kicked_players.update({player: self.players[player]})

        for player in self.players.values():
            player.add_destroyers()

        result = self.__bank.proceed_build_offers(self.__current_month, self.players)
        if result:
            kicked_players = kicked_players | result

        if self.__level == 1:
            self.__level = choices(
                [1, 2, 3, 4, 5], [1 / 3, 1 / 3, 1 / 6, 1 / 12, 1 / 12]
            )[0]
        elif self.__level == 2:
            self.__level = choices(
                [1, 2, 3, 4, 5], [1 / 4, 1 / 3, 1 / 4, 1 / 12, 1 / 12]
            )[0]
        elif self.__level == 3:
            self.__level = choices(
                [1, 2, 3, 4, 5], [1 / 12, 1 / 4, 1 / 3, 1 / 4, 1 / 12]
            )[0]
        elif self.__level == 4:
            self.__level = choices(
                [1, 2, 3, 4, 5], [1 / 12, 1 / 12, 1 / 4, 1 / 3, 1 / 4]
            )[0]
        else:
            self.__level = choices(
                [1, 2, 3, 4, 5], [1 / 12, 1 / 12, 1 / 6, 1 / 3, 1 / 4]
            )[0]

        return {
            "state": self.get_state(),
            "kicked_players": kicked_players,
            "end": self.__current_month == self.max_months,
        }

    def get_state(self):
        alive_players = sum([int(i.isAlive) for i in self.players.values()])
        print(
            level(alive_players, self.__level) | {"currentMonth": self.__current_month}
        )

        return level(alive_players, self.__level) | {
            "currentMonth": self.__current_month
        }
