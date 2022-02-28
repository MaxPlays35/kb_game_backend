from copy import deepcopy
import random
from models.offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from models.player import Player


class Bank:
    def __init__(self) -> None:
        self.produce_offers: set[str] = set()
        self.build_offers: set[str] = set()
        self.auction_offers: dict[str, AuctionOffer] = {}
        self.buy_offers: dict[str, BuyOffer] = {}
        self.buy_offers_tech: dict[int, list[BuyOffer]] = {}
        self.auction_offers_tech: dict[int, list[BuyOffer]] = {}

    def proceed_produce_offer(self, current_state, offer: ProduceOffer, player: Player):
        if offer.aircrafts > player.manufactories:
            return {
                "success": False,
                "text": "You can't build more destroyers",
            }

        print(offer.to_json())

        if (
            player.money - 2000 * offer.aircrafts > 0
            and player.raw_materials >= offer.aircrafts
        ):
            if player.id in self.produce_offers:
                return {
                    "success": False,
                    "text": "You have already produced destroyers",
                }
            player.withdraw_money(2000 * offer.aircrafts)
            player.remove_raw_materials(offer.aircrafts)
            player.add_pending_destroyers(offer.aircrafts)
            self.produce_offers.add(player.id)
            return {"success": True}

        return {
            "text": "You don't have enought money or raw materials",
            "success": False,
        }

    def add_build_offer(self, offer: BuildOffer, player: Player, current_month: int):
        if player.id in self.build_offers:
            return {
                "bankrupt": False,
                "success": False,
                "text": "You have already built manufactories",
            }
        print(offer.to_json())
        if player.money - 2500 * offer.workshops > 0:
            if (
                player.manufactories
                + sum([i["workshops"] for i in player.pending_manufactories])
                + offer.workshops
                > 6
            ):
                return {
                    "bankrupt": False,
                    "success": False,
                    "text": "You can't build more manufactories ",
                }
            player.withdraw_money(2500 * offer.workshops)
            player.add_manufactories(
                {"activate_month": current_month + 4, "workshops": offer.workshops}
            )
            self.build_offers.add(player.id)
            return {"success": True, "bankrupt": False}

        return {"success": False, "bankrupt": True}

    def add_auction_offer(self, offer: AuctionOffer, player: Player):
        if not offer.player_id in self.auction_offers:
            self.auction_offers.update({offer.player_id: offer})
            if offer.price in self.auction_offers_tech:
                self.auction_offers_tech[offer.price].append(offer)
                print(offer.to_json())
            else:
                self.auction_offers_tech[offer.price] = [offer]
                print(offer.to_json())
            return {"success": True}

        return {"success": False, "text": "You have already sent auction offer"}

    def proceed_auction_offers(self, current_state, players: dict[str, Player]):
        for price in sorted(self.auction_offers_tech.keys()):
            while (
                len(self.auction_offers_tech[price]) > 0
                and current_state["maxDestroyers"] > 0
            ):
                offer: AuctionOffer = random.choice(self.auction_offers_tech[price])
                self.auction_offers_tech[price].remove(offer)
                if current_state["maxDestroyers"] >= offer.aircrafts:
                    if (
                        players[offer.player_id].destroyers - offer.aircrafts >= 0
                        and offer.price <= current_state["maxPriceDestroyer"]
                    ):
                        players[offer.player_id].add_money(
                            offer.price * offer.aircrafts
                        )
                        players[offer.player_id].remove_destroyers(offer.aircrafts)
                        current_state["maxDestroyers"] -= offer.aircrafts
                else:
                    if (
                        players[offer.player_id].money
                        - current_state["maxDestroyers"] * offer.price
                        > 0
                        and offer.price <= current_state["maxPriceDestroyer"]
                    ):
                        players[offer.player_id].add_money(
                            offer.aircrafts * offer.price
                        )
                        players[offer.player_id].remove_destroyers(
                            current_state["maxDestroyers"]
                        )
                        current_state["maxDestroyers"] = 0

        self.auction_offers = set()
        self.auction_offers_tech = {}

    def add_buy_offer(self, offer: BuyOffer, player: Player):
        if not offer.player_id in self.buy_offers:
            self.buy_offers.update({offer.player_id: offer})
            if offer.price in self.buy_offers_tech:
                self.buy_offers_tech[offer.price].append(offer)
                print(offer.to_json())
            else:
                self.buy_offers_tech[offer.price] = [offer]
                print(offer.to_json())
            return {"success": True}

        return {"success": False, "text": "You have already sent buy offer"}

    def proceed_buy_offers(self, current_state, players: dict[str, Player]):
        for price in sorted(self.buy_offers_tech.keys(), reverse=True):
            while len(self.buy_offers_tech[price]) > 0 and current_state["volume"] > 0:
                offer: BuyOffer = random.choice(self.buy_offers_tech[price])
                self.buy_offers_tech[price].remove(offer)
                if current_state["volume"] >= offer.raw_material:
                    if (
                        players[offer.player_id].money
                        - offer.price * offer.raw_material
                        > 0
                        and offer.price >= current_state["minPriceRaw"]
                    ):
                        players[offer.player_id].add_raw_materials(offer.raw_material)
                        players[offer.player_id].withdraw_money(
                            offer.price * offer.raw_material
                        )
                        current_state["volume"] -= offer.raw_material
                else:
                    if (
                        players[offer.player_id].money
                        - current_state["volume"] * offer.raw_material
                        > 0
                        and offer.price >= current_state["minPriceRaw"]
                    ):
                        players[offer.player_id].add_raw_materials(offer.raw_material)
                        players[offer.player_id].withdraw_money(
                            offer.price * current_state["volume"]
                        )
                        current_state["volume"] = 0

        self.buy_offers = set()
        self.buy_offers_tech = {}

    def proceed_build_offers(self, current_month: int, players: dict[str, Player]):
        kicked_players: dict[str, Player] = {}
        for player in players:
            workshops = players[player].pending_manufactories
            for offer in deepcopy(workshops):
                if offer["activate_month"] == current_month:
                    if not players[player].money - offer["workshops"] * 2500 > 0:
                        kicked_players.update({player: players[player]})
                        break
                    else:
                        players[player].add_pending_manufactories(offer)
                        workshops.remove(offer)

        return kicked_players

    def withdraw_money(self, player: Player, money: int = 0):
        if money:
            player.withdraw_money(money)
        else:
            return player.withdraw_money(
                300 * player.raw_materials
                + 500 * player.destroyers
                + 1000 * player.manufactories
            )

    def clear(self):
        self.produce_offers = set()
        self.build_offers = set()
