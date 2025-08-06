class Pingback:
    def __init__(self, gateway):
        self.gateway = gateway

    def validate(self, pingbackdata: str, headers: dict) -> bool:
        if not headers or not pingbackdata:
            return False

        signature_version = headers.get("X-Fasterpay-Signature-Version", "v1")

        if signature_version == "v2":
            expected_signature = self.gateway.signature().calculate_pingback_hash(pingbackdata)
            received_signature = headers.get("X-Fasterpay-Signature")
            return expected_signature == received_signature

        # Fallback to v1: compare API keys (legacy)
        api_key = headers.get("X-ApiKey")
        return api_key == self.gateway.config.private_key
    
