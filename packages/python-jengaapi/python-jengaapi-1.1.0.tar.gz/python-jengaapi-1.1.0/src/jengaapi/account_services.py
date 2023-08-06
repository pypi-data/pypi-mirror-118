import json
from datetime import date

import requests

from . import BASE_URL
from .exceptions import handle_response


class AccountServices:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': token
        }

    @staticmethod
    def _send_get_request(headers, url):
        response = requests.get(url, headers=headers)
        formatted_response = handle_response(response)
        return formatted_response

    @staticmethod
    def _send_post_request(headers, payload, url):
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def account_balance(self, signature, country_code, account_id):
        # signature = API.signature((country_code, account_id))
        self.headers["signature"] = signature
        url = BASE_URL + f'account/v2/accounts/balances/{country_code}/{account_id}'
        return self._send_get_request(headers=self.headers, url=url)

    def account_mini_statement(self, country_code, account_id, signature):
        # signature = API.signature((country_code, account_id))
        self.headers["signature"] = signature
        url = BASE_URL + f'account/v2/accounts/ministatement/{country_code}/{account_id}'
        return self._send_get_request(headers=self.headers, url=url)

    def account_inquiry_bank_accounts(self, country_code, account_no, signature):
        # signature = API.signature((country_code, account_id))
        self.headers["signature"] = signature
        url = BASE_URL + f'account/v2/accounts/search/{country_code}/{account_no}'
        return self._send_get_request(headers=self.headers, url=url)

    def opening_closing_account_balance(self, country_code, account_id, signature, balance_date=date.today()):
        str_date = balance_date.strftime("%Y-%m-%d")
        # signature = API.signature((account_id, country_code, str_date))
        self.headers["signature"] = signature
        payload = {
            "countryCode": country_code,
            "accountId": account_id,
            "date": str_date
        }
        url = BASE_URL + 'account/v2/accounts/accountbalance/query'
        return self._send_post_request(headers=self.headers, payload=payload, url=url)

    def account_full_statement(self, from_date, to_date, country_code, account_no, signature, limit=3, **kwargs):
        reference = kwargs.get("reference", None)
        serial = kwargs.get("serial", None)
        posted_date_time = kwargs.get("posted_date_time", None)
        # signature = API.signature((country_code, account_id))
        self.headers["signature"] = signature
        payload = {
            "countryCode": country_code,
            "accountNumber": account_no,
            "fromDate": from_date.strftime("%Y-%m-%d"),
            "toDate": to_date.strftime("%Y-%m-%d"),
            "limit": limit,
            "reference": reference,
            "serial": serial,
            "postedDateTime": posted_date_time,
            "date": date.today().strftime("%Y-%m-%d"),
        }
        url = BASE_URL + 'account/v2/accounts/fullstatement'
        return self._send_post_request(headers=self.headers, payload=payload, url=url)
