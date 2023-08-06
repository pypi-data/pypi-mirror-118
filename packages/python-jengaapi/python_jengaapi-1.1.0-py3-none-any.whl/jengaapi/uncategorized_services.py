import json

import requests

from . import BASE_URL
from .exceptions import generate_reference, handle_response


class UncategorizedServices:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
        self.reference_no = generate_reference()

    def purchase_airtime(self, signature, country_code, mobile_number, airtime_amount, telco):
        ref = self.reference_no
        # signature = API.signature((MERCHANT_CODE, telco, airtime_amount, ref))
        self.headers["signature"] = signature
        payload = {
            "customer": {
                "countryCode": country_code,
                "mobileNumber": mobile_number
            },
            "airtime": {
                "amount": airtime_amount,
                "reference": ref,
                "telco": telco
            }
        }
        url = BASE_URL + f'transaction/v2/airtime'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def get_forex_rates(self, country_code, currency_code):
        payload = {
            "countryCode": country_code,
            "currencyCode": currency_code
        }
        url = BASE_URL + f'transaction/v2/foreignexchangerates'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def id_search_and_verification(self, document_type, signature, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        date_of_birth = kwargs.get("date_of_birth")
        document_number = kwargs.get("document_number")
        country_code = kwargs.get("country_code")
        # signature = API.signature((MERCHANT_CODE, document_number, self.country_code))
        self.headers["signature"] = signature
        payload = {
            "identity": {
                "documentType": document_type,
                "firstName": first_name,
                "lastName": last_name,
                "dateOfBirth": date_of_birth,
                "documentNumber": document_number,
                "countryCode": country_code
            }
        }
        url = BASE_URL + f'customer/v2/identity/verify'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response
