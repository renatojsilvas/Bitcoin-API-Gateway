from datetime import datetime, timezone
from decimal import Decimal
import json

from models import BookOrder, Information, Order


class ParseInformationError(Exception):
    pass


class Walltime:
    def __init__(self, repo) -> None:
        self.repo = repo

    def get_general_info(self) -> Information:

        try:
            info = json.loads(self.repo.get_general_info())

            return Information(
                "Bitcoin",
                "BTC",
                datetime.strptime(info["last_update"], "%Y-%m-%dT%H:%M:%SZ"),
                "BRL",
                Decimal(info["BRL_XBT"]["last_inexact"]),
                Decimal(info["BRL_XBT"]["base_volume24h_inexact"]),
                Decimal(info["BRL_XBT"]["quote_volume24h_inexact"]),
                Decimal(info["BRL_XBT"]["lowest_ask_inexact"]),
                Decimal(info["BRL_XBT"]["highest_bid_inexact"]),
            )
        except json.decoder.JSONDecodeError:
            raise ParseInformationError(
                "It was not possible to parse data downloaded from Walltime"
            )

    def parse_order(self, order_str):
        if len(order_str[0].split("/")) == 1:
            price = Decimal(order_str[0])
        else:
            price = Decimal(order_str[0].split("/")[0]) / Decimal(
                order_str[0].split("/")[1]
            )

        if len(order_str[1].split("/")) == 1:
            quantity = Decimal(order_str[1])
        else:
            quantity = Decimal(order_str[1].split("/")[0]) / Decimal(
                order_str[1].split("/")[1]
            )

        return Order(price, quantity)

    def get_book_order(self) -> BookOrder:

        info = json.loads(self.repo.get_book_order())

        bid_orders = []
        for o in info["brl-xbt"]:
            bid_orders.append(self.parse_order(o))

        ask_orders = []
        for o in info["xbt-brl"]:
            ask_orders.append(self.parse_order(o))

        return BookOrder(
            "Bitcoin",
            "BTC",
            datetime.fromtimestamp(int(info["timestamp"]) / 1000, tz=timezone.utc),
            "BRL",
            bid_orders,
            ask_orders,
        )
