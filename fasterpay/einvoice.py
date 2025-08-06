import requests

class Einvoice:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.external_api_url
        self.api_key = gateway.config.private_key

    def create_invoice(self, params: dict) -> dict:
        """
        Create a new E-Invoice.

        Required headers:
            - X-ApiKey: Your private key (added automatically).

        Parameters:
            - invoice_template_id (str): Optional. ID of an existing invoice template.
            - template (dict): Optional. Object containing template data. Only one of `invoice_template_id` or `template` should be provided.
            - number (str): Optional. Unique invoice number (max 50 chars).
            - summary (str): Optional. Description (max 255 chars).
            - contact_id (str): Required. ID of the associated contact.
            - currency (str): Required. ISO-4217 currency code (e.g., 'USD').
            - due_date (str): Optional. Due date in 'YYYY-MM-DD' format.
            - discount_id or discount (str or dict): Optional. Provide only one.
            - tax_id or tax (str or dict): Optional. Provide only one.
            - items (list of dict): Required. List of item objects. Each item may include:
                - name (str, optional): Item name (max 255 chars)
                - product_id or product (str or dict): Only one required
                - price (float): Required. Unit price of the item
                - quantity (int): Required. Quantity (min 1)
                - discount_id or discount (str or dict): Optional. Only one
                - tax_id or tax (str or dict): Optional. Only one
                - deleted_at (str, optional): Set to true to delete
            - include (str): Optional. e.g. 'prices' to show custom prices in response

        Endpoint:
            POST https://business.fasterpay.com/api/external/einvoices

        Docs:
            https://docs.fasterpay.com/api#section-create-invoice

        Returns:
            dict: API response containing invoice data.
        """
        if not params.get("contact_id"):
            raise ValueError("'contact_id' is required.")
        if not params.get("currency"):
            raise ValueError("'currency' is required.")
        if not params.get("items") or not isinstance(params["items"], list):
            raise ValueError("'items' must be a non-empty list of item objects.")

        # Enforce template OR invoice_template_id (but not both)
        if params.get("template") and params.get("invoice_template_id"):
            raise ValueError("Provide either 'template' or 'invoice_template_id', not both.")

        url = f"{self.api_url}/api/external/einvoices"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
