import requests


class Subscription:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.api_url
        self.api_key = gateway.config.private_key

    def cancel(self, order_id: str) -> dict:
        """Cancel a subscription for the given order ID."""
        if not order_id:
            raise ValueError("order_id is required to cancel a subscription.")

        url = f"{self.api_url}/api/subscription/{order_id}/cancel"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json={}, headers=headers)
        response.raise_for_status()
        return response.json()
