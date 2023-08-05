import json
import logging
from abc import ABC, abstractmethod

import requests


class BaseBroker(ABC):
    logger = logging.getLogger()

    def __init__(self, token):
        self.token = token

    def request(self, side, url, payload, headers, timeout=None):
        response = None
        try:
            response = self._request(method="POST", url=url, headers=headers, data=json.dumps(payload), timeout=timeout)
            if response.status_code == 200:
                response = response.json()
                self.logger.info(
                    f"{side} request sent successfully, {payload['isin']}, {self.__class__.__name__}: "
                    f"{response}")
                return self.parse_response(response)
            else:
                self.logger.warning(
                    f"{side} request failed, {payload['isin']}, {self.__class__.__name__}: "
                    f"status_code:{response.status_code}, response_content={response.text}")
                return False

        except Exception:
            self.logger.error(
                f"error during {side} {payload['isin']},{self.__class__.__name__}, response={response.text if response is not None else None}"
                f" {response.status_code if response is not None else None}",
                exc_info=True, )
            return False

    def _request(self, method, url, headers=None, data=None, timeout=None):
        response = requests.request(method, url, headers=headers, data=data, timeout=timeout)
        return response

    @abstractmethod
    def parse_response(self, response):
        raise NotImplemented()

    @abstractmethod
    def wait(self):
        raise NotImplemented()
