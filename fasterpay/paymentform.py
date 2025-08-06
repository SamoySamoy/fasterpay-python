import html

class PaymentForm:
    def __init__(self, gateway):
        self.gateway = gateway

    def build_form(self, parameters: dict) -> str:
        """
        Build a FasterPay Checkout Form to redirect the customer to the payment widget.

        Parameters:
            parameters (dict): A dictionary with the following structure:

            Required keys inside `parameters["payload"]`:
                - amount (str): Payment amount in "0000.00" format.
                - currency (str): ISO 4217 currency code (e.g., 'USD').
                - description (str): Description of the product.
                - api_key (str): Automatically added using your FasterPay public key.
                - merchant_order_id (str): Unique merchant-side order ID.

            Optional keys inside `payload`:
                - sign_version (str): Signature version to use ('v1' or 'v2'). Default is 'v1'.
                - email (str): Customer email.
                - first_name (str): Customer first name.
                - last_name (str): Customer last name.
                - city (str): Customer city.
                - zip (str): Customer zip/postal code.
                - payment_flow (str): Set to "user_qr" to request a QR code.
                - success_url (str): URL to redirect to after successful payment.
                - pingback_url (str): Overrides default pingback URL.
                - hash (str): Automatically calculated by the SDK using your private key.

            Top-level keys in `parameters`:
                - auto_submit_form (bool): If True, auto-submits the form via JavaScript after rendering.

        Notes:
            - `api_key` and `hash` are automatically added by this method.
            - If `sign_version` is not provided, version "v1" is used.
            - To use QR code flow, ensure `payment_flow` = "user_qr" and add header Accept: application/json (not handled here).

        Returns:
            str: A string of HTML `<form>` content that posts to FasterPay checkout endpoint.

        Docs:
            https://docs.fasterpay.com/api#section-custom-integration
        """
        payload = parameters.get("payload", {})
        payload["api_key"] = self.gateway.config.public_key

        sign_version = payload.get("sign_version", "v1")    
        payload["hash"] = self.gateway.signature().calculate_hash(payload, sign_version)

        form_fields = "\n".join(
            f'<input type="hidden" name="{html.escape(str(k))}" value="{html.escape(str(v))}" />'
            for k, v in payload.items()
        )

        form = f'''
            <form align="center" method="post" action="{self.gateway.config.api_url}/payment/form">
            {form_fields}
            <input type="Submit" value="Pay Now" id="fasterpay-submit"/>
            </form>
            '''.strip()

        if parameters.get("auto_submit_form"):
            form += '\n<script type="text/javascript">document.getElementById("fasterpay-submit").click();</script>'

        return form
    
    