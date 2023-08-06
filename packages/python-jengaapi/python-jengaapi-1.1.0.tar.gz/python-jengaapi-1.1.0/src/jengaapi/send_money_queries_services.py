import json

import requests

from . import BASE_URL
from .exceptions import handle_response


class SendMoneyQueriesServices:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }

    def account_inquiry(self, mobile_number):
        url = BASE_URL + 'transaction/v2/pesalink/inquire'
        payload = {
            "mobileNumber": mobile_number
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def transaction_status(self, request_id, destination_type, transfer_date):
        url = BASE_URL + 'transaction/v2/b2c/status/query'
        payload = {
            "requestId": request_id,
            "destination": {
                "type": destination_type
            },
            "transfer": {
                "date": transfer_date.strftime("%Y-%m-%d")
            }}
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response
