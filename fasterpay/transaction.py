import requests


class Transaction:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.api_url
        self.api_key = gateway.config.private_key

    def refund(self, order_id: str, amount: float):
        """Process a refund for a given order ID."""
        if not order_id or amount < 0:
            raise ValueError("order_id is required and amount must be non-negative.")

        url = f"{self.api_url}/payment/{order_id}/refund"
        data = {"amount": amount}
        return self._post_json(url, data)

    def deliver(self, delivery_info: dict):
        """
        Send delivery confirmation for a completed payment.

        This confirms to FasterPay that the purchased goods or services have been delivered.
        Typically used for digital goods or subscriptions after successful payment.

        Parameters:
            delivery_info (dict): A dictionary containing delivery details. Example fields:
                - payment_id (str): Required. The FasterPay payment ID.
                - merchant_reference_id (str): Optional. Your internal reference ID.
                - status (str): Required. Delivery status. Example: "delivered".
                - type (str): Optional. Type of delivery. Example: "digital".
                - estimated_delivery_datetime (str): Optional. ISO 8601 timestamp of estimated delivery time.

        Endpoint:
            POST https://pay.fasterpay.com/api/v1/deliveries

        Docs:
            https://docs.fasterpay.com/api#section-delivery-confirmation (update with actual link)

        Returns:
            dict: API response confirming delivery has been recorded.
        """
        url = f"{self.api_url}/api/v1/deliveries"
        return self._post_json(url, delivery_info)


    def _post_json(self, url: str, data: dict):
        """Helper to POST JSON with auth header."""
        headers = {"X-ApiKey": self.api_key, "Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    