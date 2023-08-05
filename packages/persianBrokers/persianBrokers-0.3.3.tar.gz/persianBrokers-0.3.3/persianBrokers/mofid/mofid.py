import time
import uuid

from persiantools.jdatetime import JalaliDate

from persianBrokers.base_broker import BaseBroker


def today_persian_date():
    today = JalaliDate.today()
    return f"{today.year}/{today.month}/{today.day}"


def get_reference_key():
    return str(uuid.uuid4())


class Mofid(BaseBroker):
    def buy(self, isin, order_count, order_price, timeout=None):
        url = "https://api.cl3.mofid.dev/easy/api/OmsOrder"

        payload = {
            "isin": isin,
            "financeId": 1,
            "quantity": order_count,
            "price": order_price,
            "side": 0,
            "validityType": 74,
            "validityDateJalali": today_persian_date(),
            "easySource": 1,
            "referenceKey": get_reference_key(),
            "cautionAgreementSelected": False
        }
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }

        return self.request(side='buy', url=url, payload=payload, headers=headers, timeout=timeout)

    def sell(self, isin, order_count, order_price, timeout=None):
        url = "https://api.cl3.mofid.dev/easy/api/OmsOrder"

        payload = {
            "isin": isin,
            "financeId": 1,
            "quantity": order_count,
            "price": order_price,
            "side": 1,
            "validityType": 74,
            "validityDateJalali": today_persian_date(),
            "easySource": 1,
            "referenceKey": get_reference_key(),
            "cautionAgreementSelected": False
        }
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }
        return self.request(side='sell', url=url, payload=payload, headers=headers, timeout=timeout)

    def parse_response(self, response: dict) -> bool:
        return response.get('isSuccessfull', False)

    def wait(self):
        time.sleep(0.300)