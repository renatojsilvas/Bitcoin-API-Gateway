from datetime import datetime, timezone
from decimal import Decimal
from exchanges.walltime import ParseInformationError, Walltime
from models import BookOrder, Information, Order
from repositories.walltime import WalltimeRepository
import pytest


def test_get_information_succesfully(mocker):
    expected = Information(
        "Bitcoin",
        "BTC",
        datetime.strptime("2022-04-11T08:13:31Z", "%Y-%m-%dT%H:%M:%SZ"),
        "BRL",
        Decimal("200000.0"),
        Decimal("6329.47983432188"),
        Decimal("0.0314698406688121"),
        Decimal("204990.0"),
        Decimal("200000.0"),
    )

    def get_general_info():
        return """
        { 
            "version":"1",
            "last_update":"2022-04-11T08:13:31Z",
            "last_update_timestamp":"1649664811722",
            "BRL_XBT":{
                "last_inexact":"200000.0",
                "last":"200000",
                "highest_bid_inexact":"200000.0",
                "highest_bid":"200000",
                "n_trades_24h":"26",
                "lowest_ask_inexact":"204990.0",
                "lowest_ask":"204990",
                "base_volume24h_inexact":"6329.47983432188",
                "base_volume24h":"63294798343218799999/10000000000000000",
                "quote_volume24h_inexact":"0.0314698406688121",
                "quote_volume24h":"314698406688121/10000000000000000",
                "base_volume_today_inexact":"3364.7314256764435",
                "base_volume_today":"33647314256764435371/10000000000000000",
                "quote_volume_today_inexact":"0.0167982355661752",
                "quote_volume_today":"20997794457719/1250000000000000",
                "base_volume_yesterday_inexact":"2964.7484086454365",
                "base_volume_yesterday":"7411871021613591157/2500000000000000",
                "quote_volume_yesterday_inexact":"0.0146716051026369",
                "quote_volume_yesterday":"146716051026369/10000000000000000"
            }
        }"""

    repository = WalltimeRepository()
    repository.get_general_info = get_general_info

    walltime = Walltime(repository)

    info = walltime.get_general_info()

    assert info == expected


def test_get_information_unsuccesfully(mocker):
    def get_general_info():
        return "wrong-response"

    repository = WalltimeRepository()
    repository.get_general_info = get_general_info

    walltime = Walltime(repository)

    with pytest.raises(
        ParseInformationError,
        match=r"It was not possible to parse data downloaded from Walltime",
    ):
        walltime.get_general_info()


def test_get_book_order_one_succesfully():
    expected = BookOrder(
        "Bitcoin",
        "BTC",
        datetime.strptime(
            "2022-04-15T11:44:39.931000Z+00:00", "%Y-%m-%dT%H:%M:%S.%fZ%z"
        ),
        "BRL",
        [
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            )
        ],
        [
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            )
        ],
    )

    def get_book_order():
        return """{
                    "timestamp":1650023079931,
                    "xbt-brl":[    
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ]
                    ],
                    "brl-xbt":[    
                        [
                        "3337/100",
                        "3337/18865000"
                        ]   
                    ]
                }"""

    repository = WalltimeRepository()
    repository.get_book_order = get_book_order

    walltime = Walltime(repository)

    info = walltime.get_book_order()

    assert info == expected


def test_get_book_order_two_succesfully():
    expected = BookOrder(
        "Bitcoin",
        "BTC",
        datetime.strptime(
            "2022-04-15T11:44:39.931000Z+00:00", "%Y-%m-%dT%H:%M:%S.%fZ%z"
        ),
        "BRL",
        [
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            ),
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            ),
        ],
        [
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            ),
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            ),
        ],
    )

    def get_book_order():
        return """{
                    "timestamp":1650023079931,
                    "xbt-brl":[    
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ],
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ]
                    ],
                    "brl-xbt":[    
                                [
                                "3337/100",
                                "3337/18865000"
                                ],
                                [
                                "3337/100",
                                "3337/18865000"
                                ]   
                    ]
                }"""

    repository = WalltimeRepository()
    repository.get_book_order = get_book_order

    walltime = Walltime(repository)

    info = walltime.get_book_order()

    assert info == expected


def test_get_book_order_three_succesfully():
    expected = BookOrder(
        "Bitcoin",
        "BTC",
        datetime.strptime(
            "2022-04-15T11:44:39.931000Z+00:00", "%Y-%m-%dT%H:%M:%S.%fZ%z"
        ),
        "BRL",
        [
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            ),
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            ),
            Order(
                Decimal("3337") / Decimal("100"), Decimal("3337") / Decimal("18865000")
            ),
        ],
        [
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            ),
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            ),
            Order(
                Decimal("67279") / Decimal("20000000"),
                Decimal("1345579932721") / Decimal("2000000000"),
            ),
        ],
    )

    def get_book_order():
        return """{
                    "timestamp":1650023079931,
                    "xbt-brl":[    
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ],
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ],
                                [
                                "67279/20000000",
                                "1345579932721/2000000000"
                                ]
                    ],
                    "brl-xbt":[    
                                [
                                "3337/100",
                                "3337/18865000"
                                ],
                                [
                                "3337/100",
                                "3337/18865000"
                                ],
                                [
                                "3337/100",
                                "3337/18865000"
                                ]   
                    ]
                }"""

    repository = WalltimeRepository()
    repository.get_book_order = get_book_order

    walltime = Walltime(repository)

    info = walltime.get_book_order()

    assert info == expected
