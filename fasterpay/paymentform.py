import html

class PaymentForm:
    def __init__(self, gateway):
        self.gateway = gateway

    def build_form(self, parameters: dict) -> str:
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
    
    