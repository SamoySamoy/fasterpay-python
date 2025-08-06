import requests

class Contact:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.external_api_url
        self.api_key = gateway.config.private_key

    def create_contact(self, params: dict) -> dict:
        """
        Create a new contact.

        Parameters (at least one of `email` or `phone` is required):
            - email (str): Email address of the contact.
            - phone (str): Phone number of the contact.
            - phone_country_code (str): Required if phone is provided. ISO 3166-1 alpha-2 format (e.g., 'US').
            - first_name (str, optional): Max 90 characters.
            - last_name (str, optional): Max 90 characters.
            - country (str, optional): ISO 3166-1 alpha-2 code.
            - favorite (bool, optional): Mark this contact as favorite.

        Endpoint:
            POST https://business.fasterpay.com/api/external/contacts

        Docs:
            https://docs.fasterpay.com/api#section-create-contact

        Returns:
            dict: Contact creation result.
        """
        email = params.get("email")
        phone = params.get("phone")
        phone_code = params.get("phone_country_code")

        if not email and not phone:
            raise ValueError("Either 'email' or 'phone' is required.")

        if phone and not phone_code:
            raise ValueError("'phone_country_code' is required when 'phone' is provided.")

        url = f"{self.api_url}/api/external/contacts"
        response = requests.post(url, json=params)
        response.raise_for_status()
        return response.json()

    def list_contacts(self, params: dict = None) -> dict:
        """
        Retrieve a list of contacts with optional filtering and sorting.

        Optional Parameters:
            - prefer_favorite (bool): Show favorite contacts first.
            - fasterpay_account_only (bool): Show only contacts with FasterPay accounts.
            - name (str): Filter by full name (first or last name).
            - email (str): Filter by email prefix.
            - phone (str): Filter by phone number.
            - country (str): Filter by ISO 3166-1 alpha-2 country code.
            - sort_by (str): Required if `order_by` is present. One of: first_name, last_name, favorite, updated_at, last_transfer_at.
            - order_by (str): Required if `sort_by` is present. One of: asc, desc.
            - page (int): Page number to retrieve (default 1).
            - per_page (int): Max records per page (max 1000).

        Endpoint:
            GET https://business.fasterpay.com/api/external/contacts

        Docs:
            https://docs.fasterpay.com/api#section-contact-list

        Returns:
            dict: Paginated list of contacts.
        """
        params = params or {}

        if "sort_by" in params and "order_by" not in params:
            raise ValueError("'order_by' is required when 'sort_by' is provided.")
        if "order_by" in params and "sort_by" not in params:
            raise ValueError("'sort_by' is required when 'order_by' is provided.")

        url = f"{self.api_url}/api/external/contacts"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_contact(self, contact_id: str) -> dict:
        """
        Retrieve details of a specific contact by ID.

        Parameters:
            - contact_id (str): ID of the contact (e.g., CT-250527-AZARCIJE)

        Endpoint:
            GET https://business.fasterpay.com/api/external/contacts/{contact_id}

        Returns:
            dict: Contact detail response.
        """
        if not contact_id:
            raise ValueError("contact_id is required to retrieve a contact.")

        url = f"{self.api_url}/api/external/contacts/{contact_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def update_contact(self, contact_id: str, params: dict) -> dict:
        """
        Update a contact's details.

        Parameters:
            - contact_id (str): ID of the contact to update.
            - params (dict): Fields to update:
                - email (str, optional)
                - phone (str, optional)
                - phone_country_code (str): Required if phone is present.
                - first_name (str, optional)
                - last_name (str, optional)
                - country (str, optional)
                - favorite (bool, optional)

        Endpoint:
            PUT https://business.fasterpay.com/api/external/contacts/{contact_id}

        Returns:
            dict: Updated contact info.
        """
        if not contact_id:
            raise ValueError("contact_id is required to update a contact.")

        url = f"{self.api_url}/api/external/contacts/{contact_id}"
        response = requests.put(url, json=params)
        response.raise_for_status()
        return response.json()

    def delete_contact(self, contact_id: str) -> dict:
        """
        Delete a contact by ID.

        Parameters:
            - contact_id (str): ID of the contact to delete.

        Endpoint:
            DELETE https://business.fasterpay.com/api/external/contacts/{contact_id}

        Returns:
            dict: API response with success status.
        """
        if not contact_id:
            raise ValueError("contact_id is required to delete a contact.")

        url = f"{self.api_url}/api/external/contacts/{contact_id}"
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
