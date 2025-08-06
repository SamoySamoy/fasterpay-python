import requests


class Address:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.external_api_url

    def get_address(self, country_code: str) -> dict:
        """Retrieve the address fields required for the specified country."""
        if not country_code:
            raise ValueError("country_code is required to retrieve address fields.")

        url = f"{self.api_url}/api/external/address/fields/{country_code}"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()
