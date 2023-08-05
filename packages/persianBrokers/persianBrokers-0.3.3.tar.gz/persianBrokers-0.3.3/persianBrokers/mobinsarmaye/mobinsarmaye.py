import time

from persianBrokers.base_broker import BaseBroker


class Mobinsarmaye(BaseBroker):
    def buy(self, isin: str, order_count: int, order_price: int, timeout=None):
        url = "https://api3.mobinsb.ir/web/v1/Order/Post"

        payload = {
            "orderCount": order_count,
            "orderPrice": order_price,
            "FinancialProviderId": 1,
            "isin": isin,
            "orderSide": 65,
            "orderValidity": 74,
            "orderValiditydate": "",
            "maxShow": 0,
            "orderId": 0
        }
        headers = {
            'Authorization': F'BasicAuthentication {self.token}',
            'Content-Type': 'application/json',
        }
        return self.request(side='buy', url=url, payload=payload, headers=headers, timeout=timeout)

    def sell(self, isin, order_count, order_price, timeout=None):
        url = "https://api3.mobinsb.ir/web/v1/Order/Post"

        payload = {
            "orderCount": order_count,
            "orderPrice": order_price,
            "FinancialProviderId": 1,
            "isin": isin,
            "orderSide": 86,
            "orderValidity": 74,
            "orderValiditydate": "",
            "maxShow": 0,
            "orderId": 0
        }
        headers = {
            'Authorization': F'BasicAuthentication {self.token}',
            'Content-Type': 'application/json',
        }
        return self.request(side='sell', url=url, payload=payload, headers=headers, timeout=timeout)

    def parse_response(self, response: dict) -> bool:
        return response.get('IsSuccessfull', False)

    def wait(self):
        pass