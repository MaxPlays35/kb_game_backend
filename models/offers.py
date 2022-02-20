from dataclasses import dataclass


@dataclass
class BuyOffer:
    player_id: str
    raw_material: int
    price: int


@dataclass
class ProduceOffer:
    player_id: str
    aircrafts: int
    price = 2000


@dataclass
class BuildOffer:
    player_id: str
    workshops: int
    price = 5000


@dataclass
class AuctionOffer:
    player_id: str
    aircrafts: int
    price: int
