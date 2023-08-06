import json

import requests

from . import BASE_URL

from .exceptions import generate_reference, handle_response


class ReceiveMoneyService:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
        self.reference_no = generate_reference()

    def receive_payments_eazzypay_push(self, signature, **kwargs):
        # signature = API.signature((self.reference_no, payment_amount,
        #                            merchant_code, country_code))
        mobile_number = kwargs.get("mobile_number")
        description = kwargs.get("description")
        country_code = kwargs.get("country_code")
        payment_amount = kwargs.get("payment_amount")

        self.headers["signature"] = signature
        payload = {
            "customer": {
                "mobileNumber": mobile_number,
                "countryCode": country_code
            },
            "transaction": {
                "amount": payment_amount,
                "description": description,
                "type": "EazzyPayOnline",
                "reference": self.reference_no
            }
        }
        url = BASE_URL + 'transaction/v2/payments'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def receive_payments_bill_payments(self, signature, **kwargs):
        reference_no = kwargs.get("reference_no", self.reference_no)
        partner_id = kwargs.get("partner_id")
        payer_name = kwargs.get("payer_name")
        account = kwargs.get("account")
        payer_mobile_number = kwargs.get("payer_mobile_number")
        biller_code = kwargs.get("biller_code")
        country_code = kwargs.get("country_code")
        payment_amount = kwargs.get("payment_amount")
        currency_code = kwargs.get("currency_code")
        remarks = kwargs.get("remarks")
        # signature = API.signature((biller_code, self.payment_amount,
        #                            ref, partner_id))
        self.headers["signature"] = signature

        payload = {
            "biller": {
                "billerCode": biller_code,
                "countryCode": country_code
            },
            "bill": {
                "reference": reference_no,
                "amount": payment_amount,
                "currency": currency_code
            },
            "payer": {
                "name": payer_name,
                "account": account,
                "reference": reference_no,
                "mobileNumber": payer_mobile_number
            },
            "partnerId": partner_id,
            "remarks": remarks
        }
        url = BASE_URL + 'transaction/v2/bills/pay'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def receive_payments_merchant_payments(self, signature, **kwargs):
        reference_no = kwargs.get("reference_no", self.reference_no)
        merchant_till = kwargs.get("merchant_till")
        payment_amount = kwargs.get("payment_amount")
        country_code = kwargs.get("country_code")
        partner_id = kwargs.get("partner_id")
        # signature = API.signature((merchant_till, self.partner_id,
        #                            self.payment_amount, self.currency_code, ref))
        self.headers["signature"] = signature

        payload = {
            "merchant": {
                "till": merchant_till
            },
            "payment": {
                "ref": reference_no,
                "amount": payment_amount,
                "currency": country_code
            },
            "partner": {
                "id": partner_id,
                "ref": reference_no
            }
        }
        url = BASE_URL + 'transaction/v2/tills/pay'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    def bill_validation(self, **kwargs):
        biller_code = kwargs.get("biller_code")
        customer_ref_number = kwargs.get("customer_ref_number")
        payment_amount = kwargs.get("payment_amount")
        currency_code = kwargs.get("currency_code")
        payload = {
            "billerCode": biller_code,
            "customerRefNumber": customer_ref_number,
            "amount": payment_amount,
            "amountCurrency": currency_code
        }
        url = BASE_URL + 'transaction/v2/tills/pay'
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response
