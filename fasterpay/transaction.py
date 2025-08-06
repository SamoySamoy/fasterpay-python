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
        """Send delivery confirmation."""
        url = f"{self.api_url}/api/v1/deliveries"
        return self._post_json(url, delivery_info)

    def _post_json(self, url: str, data: dict):
        """Helper to POST JSON with auth header."""
        headers = {"X-ApiKey": self.api_key, "Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    