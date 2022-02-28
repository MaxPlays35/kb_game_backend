from dataclasses import dataclass


@dataclass
class BuyOffer:
    player_id: str
    raw_material: int
    price: int

    def to_json(self):
        return {
            "player_id": self.player_id,
            "raw_material": self.raw_material,
            "price": self.price,
            "type": "BuyOffer",
        }


@dataclass
class ProduceOffer:
    player_id: str
    aircrafts: int
    price = 2000

    def to_json(self):
        return {
            "player_id": self.player_id,
            "aircrafts": self.aircrafts,
            "type": "ProduceOffer",
        }


@dataclass
class BuildOffer:
    player_id: str
    workshops: int
    price = 5000

    def to_json(self):
        return {
            "player_id": self.player_id,
            "workshops": self.workshops,
            "price": self.price,
            "type": "BuildOffer",
        }


@dataclass
class AuctionOffer:
    player_id: str
    aircrafts: int
    price: int

    def to_json(self):
        return {
            "player_id": self.player_id,
            "aircrafts": self.aircrafts,
            "price": self.price,
            "type": "AuctionOffer",
        }
