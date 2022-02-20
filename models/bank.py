from models.offers import AuctionOffer, BuildOffer, BuyOffer, ProduceOffer


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
