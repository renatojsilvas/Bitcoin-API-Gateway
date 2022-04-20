from datetime import datetime
from decimal import Decimal
from typing import List
from dataclasses import dataclass


@dataclass
class Order:
    price: Decimal
    quantity: Decimal


@dataclass
class MetaData:
    name: str
    symbol: str
    info_date: datetime
    currency: str


@dataclass
class Information(MetaData):
    last_price: Decimal
    base_volume_24h: Decimal
    quote_volume_24h: Decimal
    lowest_ask: Decimal
    highest_bid: Decimal


@dataclass
class BookOrder(MetaData):
    order_book_bid: List[Order]
    order_book_ask: List[Order]
