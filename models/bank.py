from models.offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from models.player import Player


class Bank:
    def __init__(self) -> None:
        self.produce_offers: set[str] = set()
        self.build_offers: set[str] = set()
        self.auction_offers: dict[str, AuctionOffer] = {}
        self.buy_offers: dict[str, BuyOffer] = {}

    def proceed_produce_offer(self, offer: ProduceOffer, player: Player):
        if offer.aircrafts > player.manufactories:
            return {
                "success": False,
                "text": "You can't build more destroyers",
            }

        if player.money - 2000 * offer.aircrafts > 0:
            if player.id in self.produce_offers:
                return {
                    "success": False,
                    "text": "You have already produced destroyers",
                }
            player.withdraw_money(2000 * offer.aircrafts)
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
        if player.money - 2500 * offer.workshops > 0:
            if (
                player.manufactories
                + sum([i.items()[1] for i in player.__pending_manufactories])
                + offer.workshops
                > 6
            ):
                return {
                    "bankrupt": False,
                    "success": False,
                    "text": "You can't build more manufactories ",
                }
            player.withdraw_money(2500 * offer.workshops)
            player.add_manufactories({current_month + 4: offer.workshops})
            self.build_offers.add(player.id)
            return {"success": True, "bankrupt": False}

        return {"success": False, "bankrupt": True}

    def add_auction_offer(self, offer: AuctionOffer):
        if not offer.player_id in self.auction_offers:
            self.auction_offers.update({offer.player_id: offer})
            return {"success": True}

        return {"success": False, "text": "You have already sent auction offer"}

    def add_buy_offer(self, offer: BuyOffer):
        if not offer.player_id in self.buy_offers:
            self.buy_offers.update({offer.player_id: offer})
            return {"success": True}

        return {"success": False, "text": "You have already sent buy offer"}

    def proceed_buy_offers(self, current_state, players: list[Player]):
        pass

    def withdraw_money(self, player: Player, money: int = 0):
        if money:
            player.withdraw_money(money)
        else:
            player.withdraw_money(
                300 * player.raw_materials
                + 500 * player.destroyers
                + 1000 * player.manufactories
            )
