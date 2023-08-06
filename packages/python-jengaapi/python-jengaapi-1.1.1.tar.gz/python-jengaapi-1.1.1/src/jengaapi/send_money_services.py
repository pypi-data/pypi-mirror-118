import json

import requests

from . import BASE_URL
from .exceptions import handle_response, generate_reference


class SendMoneyService:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
        self.reference_no = generate_reference()

    @staticmethod
    def _generate_payload_source(country_code, source_name, source_account_number):
        return dict(
            countryCode=country_code,
            name=source_name,
            accountNumber=source_account_number
        )

    @staticmethod
    def _generate_payload_destination(country_code, destination_name):
        return dict(
            type=None,
            countryCode=country_code,
            name=destination_name,
        )

    @staticmethod
    def _generate_payload_transfer(transfer_amount, currency_code, reference_no,
                                   transfer_date, description):
        return dict(
            type=None,
            amount=str(transfer_amount),
            currencyCode=currency_code,
            reference=reference_no,
            date=transfer_date.strftime("%Y-%m-%d"),
            description=description
        )

    @staticmethod
    def _send_request(headers, payload):
        url = BASE_URL + f'transaction/v2/remittance'
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        formatted_response = handle_response(response)
        return formatted_response

    @staticmethod
    def _redundant_params(kwargs):
        country_code = kwargs.get("country_code")
        source_name = kwargs.get("source_name")
        source_account_number = kwargs.get("source_account_number")
        destination_name = kwargs.get("destination_name")
        transfer_amount = kwargs.get("transfer_amount")
        currency_code = kwargs.get("currency_code")
        reference_no = kwargs.get("reference_no")
        transfer_date = kwargs.get("transfer_date")
        description = kwargs.get("description")
        return (country_code, source_name, source_account_number, destination_name,
                transfer_amount, currency_code, reference_no, transfer_date, description)

    def send_within_equity(self, signature, **kwargs):
        destination_account_number = kwargs.get("destination_account_number")

        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)

        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)
        self.headers["signature"] = signature
        payload_destination["type"] = "bank"
        payload_destination["accountNumber"] = destination_account_number
        payload_transfer["type"] = "InternalFundsTransfer"
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_to_mobile_wallets(self, signature, **kwargs):
        wallet_name = kwargs.get("wallet_name")
        destination_mobile_number = kwargs.get("destination_mobile_number")
        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)
        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)
        self.headers["signature"] = signature
        payload_destination["type"] = "mobile"
        payload_destination["mobileNumber"] = destination_mobile_number
        payload_destination["walletName"] = wallet_name
        payload_transfer["type"] = "MobileWallet"
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_rtgs(self, signature, **kwargs):
        destination_account_number = kwargs.get("destination_account_number")
        bank_code = kwargs.get("bank_code")

        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)

        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)

        self.headers["signature"] = signature
        payload_destination["type"] = "bank"
        payload_destination["bankCode"] = bank_code
        payload_destination["accountNumber"] = destination_account_number
        payload_transfer["type"] = "RTGS"
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_swift(self, signature, **kwargs):
        bank_bic = kwargs.get('bank_bic')
        address_line = kwargs.get('address_line')
        charge_option = kwargs.get('charge_option')
        destination_account_number = kwargs.get('destination_account_number')
        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)
        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)

        self.headers["signature"] = signature
        payload_destination["type"] = "bank"
        payload_destination["bankBic"] = bank_bic
        payload_destination["accountNumber"] = destination_account_number
        payload_destination["addressline1"] = address_line
        payload_transfer["type"] = "SWIFT"
        payload_transfer["chargeOption"] = charge_option
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_eft(self, signature, **kwargs):
        bank_code = kwargs.get('bank_code')
        branch_code = kwargs.get('branch_code')
        destination_account_number = kwargs.get('destination_account_number')

        # signature = API.signature((self.reference_no, self.source_account_number,
        #                            destination_account_number, self.transfer_amount,
        #                            bank_code))

        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)

        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)

        self.headers["signature"] = signature
        payload_destination["type"] = "bank"
        payload_destination["bankCode"] = bank_code
        payload_destination["branchCode"] = branch_code
        payload_destination["accountNumber"] = destination_account_number
        payload_transfer["type"] = "EFT"
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_pesalink_to_bank_account(self, signature, **kwargs):
        bank_code = kwargs.get('bank_code')
        mobile_number = kwargs.get('mobile_number')
        destination_account_number = kwargs.get('destination_account_number')

        # signature = API.signature((self.transfer_amount, self.currency_code, self.reference_no,
        #                            self.destination_name, self.source_account_number))

        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)

        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)

        self.headers["signature"] = signature
        payload_destination["type"] = "bank"
        payload_destination["bankCode"] = bank_code
        payload_destination["mobileNumber"] = mobile_number
        payload_destination["accountNumber"] = destination_account_number
        payload_transfer["type"] = "PesaLink"
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)

    def send_pesalink_to_mobile_number(self, signature, **kwargs):
        destination_mobile_number = kwargs.get("destination_mobile_number")
        bank_code = kwargs.get("bank_code")
        # signature = API.signature((self.transfer_amount, self.currency_code,
        #                            self.reference_no, self.destination_name,
        #                            self.source_account_number))

        (country_code, source_name, source_account_number, destination_name,
         transfer_amount, currency_code, reference_no, transfer_date, description) = self._redundant_params(kwargs)

        payload_destination = self._generate_payload_destination(country_code, destination_name)
        payload_source = self._generate_payload_source(country_code, source_name, source_account_number)
        payload_transfer = self._generate_payload_transfer(transfer_amount, currency_code,
                                                           reference_no, transfer_date, description)

        self.headers["signature"] = signature
        payload_destination["type"] = "mobile"
        payload_destination["bankCode"] = bank_code
        payload_destination["mobileNumber"] = destination_mobile_number
        payload = dict(source=payload_source,
                       destination=payload_destination,
                       transfer=payload_transfer)
        return self._send_request(headers=self.headers, payload=payload)
