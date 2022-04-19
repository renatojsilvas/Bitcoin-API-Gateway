import secrets
import requests
import json

URL_BASE = "https://s3.amazonaws.com/data-production-walltime-info/production/dynamic"


class ProviderUnavaliableError(Exception):
    pass


class WalltimeRepository:
    def nonce(self):
        return secrets.token_hex(32)

    def get(self, url):
        response = requests.get(url)

        if response.status_code == 503:
            raise ProviderUnavaliableError("Walltime provider is not available")

        if response.status_code == 200:
            return response.content

    def get_general_info(self):
        resource = "walltime-info.json"

        return self.get(f"{URL_BASE}/{resource}?now={self.nonce()}")

    def get_book_order(self):
        meta = self.get_meta()
        current_round = json.loads(meta)["current_round"]
        order_book_prefix = json.loads(meta)["order_book_prefix"]

        resource = f"{order_book_prefix}_r{current_round}_p0.json"

        return self.get(f"{URL_BASE}/{resource}?now={self.nonce()}")

    def get_meta(self):
        resource = "meta.json"

        return self.get(f"{URL_BASE}/{resource}?now={self.nonce()}")
