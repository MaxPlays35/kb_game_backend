from models.offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer
from models.player import Player


class Bank:
    def __init__(self) -> None:
        self.produce_offers: list[ProduceOffer] = []
        self.build_offers: list[BuildOffer] = []
        self.auction_offers: list[AuctionOffer] = []
        self.buy_offers: list[BuyOffer] = []

    def add_produce_offer(self, offer: ProduceOffer):
        self.produce_offers.append(offer)

    def add_build_offer(self, offer: BuildOffer):
        self.build_offers.append(offer)

    def add_auction_offer(self, offer: AuctionOffer):
        self.auction_offers.append(offer)

    def add_buy_offer(self, offer: BuyOffer):
        self.buy_offers.append(offer)

    def withdraw_money(self, player: Player, money: int = 0):
        if money:
            player.withdraw_money(money)
        else:
            player.withdraw_money(
                300 * player.raw_materials
                + 500 * player.destroyers
                + 1000 * player.manufactories
            )
