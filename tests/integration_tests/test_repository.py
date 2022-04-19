import json

import pytest
from repositories.walltime import ProviderUnavaliableError, WalltimeRepository


def test_get_information_from_walltime_succesfully():
    walltime_repository = WalltimeRepository()

    general_info = walltime_repository.get_general_info()

    assert json.loads(general_info)["version"] == "1"


def test_get_information_from_walltime_unsuccesfully_because_is_unavaliable(
    requests_mock,
):
    nonce = "1528962473468.679.0000000000873"

    walltime_repository = WalltimeRepository()
    walltime_repository.nonce = lambda: nonce

    requests_mock.get(
        f"https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/walltime-info.json?now={nonce}",
        status_code=503,
    )

    with pytest.raises(
        ProviderUnavaliableError, match="Walltime provider is not available"
    ):
        walltime_repository.get_general_info()


def test_get_book_order_from_walltime_succesfully():
    walltime_repository = WalltimeRepository()

    json_response = walltime_repository.get_book_order()

    book_order = json.loads(json_response)

    assert book_order["timestamp"] != "0"


def test_get_book_order_from_walltime_unsuccesfully_because_meta_is_unavaliable(
    requests_mock,
):
    nonce = "1528962473468.679.0000000000873"

    walltime_repository = WalltimeRepository()
    walltime_repository.nonce = lambda: nonce

    requests_mock.get(
        f"https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/meta.json?now={nonce}",
        status_code=503,
    )

    with pytest.raises(
        ProviderUnavaliableError, match="Walltime provider is not available"
    ):
        walltime_repository.get_meta()


def test_get_book_order_from_walltime_unsuccesfully_because_order_book_is_unavaliable(
    requests_mock,
):
    nonce = "1528962473468.679.0000000000873"
    current_round = 1490454
    order_book_prefix = "order-book/v8878cb"

    walltime_repository = WalltimeRepository()
    walltime_repository.nonce = lambda: nonce
    walltime_repository.get_meta = (
        lambda: '{"current_round": 1490454, "order_book_prefix": "order-book/v8878cb"}'
    )

    requests_mock.get(
        f"https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/{order_book_prefix}_r{current_round}_p0.json?now={nonce}",
        status_code=503,
    )

    with pytest.raises(
        ProviderUnavaliableError, match="Walltime provider is not available"
    ):
        walltime_repository.get_book_order()
