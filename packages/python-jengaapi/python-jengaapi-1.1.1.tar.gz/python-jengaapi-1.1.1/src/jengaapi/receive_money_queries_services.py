import requests

from . import BASE_URL
from .exceptions import handle_response


class ReceiveMoneyQueriesService:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }

    def get_all_eazzy_pay_merchants(self, per_page, page):
        url = BASE_URL + f'transaction/v2/merchants?per_page={per_page}&page={page}'
        response = requests.get(url, headers=self.headers)
        formatted_response = handle_response(response)
        return formatted_response

    def get_payment_status_eazzy_pay_push(self, transaction_ref):
        url = BASE_URL + f'transaction/v2/payments/{transaction_ref}'
        response = requests.get(url, headers=self.headers)
        formatted_response = handle_response(response)
        return formatted_response

    def query_transaction_details(self, payments_ref):
        url = BASE_URL + f'transaction/v2/payments/details/{payments_ref}'
        response = requests.get(url, headers=self.headers)
        formatted_response = handle_response(response)
        return formatted_response

    def get_all_billers(self, per_page, page):
        url = BASE_URL + f'transaction/v2/billers?per_page={per_page}&page={page}'
        response = requests.get(url, headers=self.headers)
        formatted_response = handle_response(response)
        return formatted_response
