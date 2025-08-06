import requests

class Payout:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.external_api_url
        self.api_key = gateway.config.private_key

    def create_payout(self, params: dict) -> dict:
        """
        Create one or more payouts in a single request.

        Required headers:
            - X-ApiKey: Your private API key (set automatically).

        Parameters (in `params`):
            - source_currency (str): Required. ISO-4217 currency of your balance (e.g. 'EUR').
            - template (str): Required. Payout destination type: 'wallet' or 'bank_account'.
            - payouts (list): Required. List of payout objects. Each object includes:
                - amount (str): Required. Amount to transfer.
                - amount_currency (str): Required. Must be same as source_currency or target_currency.
                - target_currency (str): Required. ISO-4217 currency to send.
                - receiver_type (str): Required. 'private' or 'business'.
                - receiver_full_name (str): Required. Full name of recipient.
                - receiver_email (str): Optional. Recipient's FasterPay email.
                - bank_beneficiary_country (str): Required if template=bank_account.
                - bank_beneficiary_address (str): Required if template=bank_account.
                - bank_account_number (str): Required if template=bank_account.
                - bank_swift_code (str): Required if template=bank_account.
                - bank_name (str): Required if template=bank_account.
                - corresponding_bank_swift_code (str, optional)
                - additional_information (str, optional)
                - reference_id (str, optional): Unique ID in your system.

        Endpoint:
            POST https://business.fasterpay.com/api/external/payouts

        Docs:
            https://docs.fasterpay.com/api#section-create-payout

        Returns:
            dict: API response with created payout data.
        """
        if "source_currency" not in params:
            raise ValueError("'source_currency' is required")
        if "template" not in params:
            raise ValueError("'template' is required")
        if "payouts" not in params or not isinstance(params["payouts"], list):
            raise ValueError("'payouts' must be a list of payout objects")

        url = f"{self.api_url}/api/external/payouts"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def list_payouts(self) -> dict:
        """Retrieve a list of payouts."""
        url = f"{self.api_url}/api/external/payouts"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_payout(self, payout_id: str) -> dict:
        """Retrieve details of a specific payout by ID."""
        if not payout_id:
            raise ValueError("payout_id is required to retrieve a payout.")

        url = f"{self.api_url}/api/external/payouts/{payout_id}"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
