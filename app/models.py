from dataclasses import dataclass


@dataclass
class Card:
    id: int
    name: str
    image_filename: str
    real_price: float
    promo_price: float
