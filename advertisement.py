from dataclasses import dataclass
from decimal import Decimal
from car import Car


@dataclass
class Advertisement:
    id: int
    website_name: str
    ad_url: str
    photo_url: str
    price: Decimal
    car: Car
