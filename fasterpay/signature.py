from urllib.parse import urlencode
import hashlib
import hmac

class Signature:
    def __init__(self, gateway):
        self.gateway = gateway

    def _sorted_items(self, params: dict) -> list[tuple[str, str]]:
        return sorted(params.items())

    def calculate_hash(self, params: dict, scheme: str = "v1") -> str:
        if scheme == "v1":
            query_string = urlencode(self._sorted_items(params)) + self.gateway.config.private_key
            return hashlib.sha256(query_string.encode()).hexdigest()

        # v2: build manually
        encoded = "".join(f"{k}={v};" for k, v in self._sorted_items(params))
        return hmac.new(
            self.gateway.config.private_key.encode(),
            encoded.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

    def calculate_pingback_hash(self, pingback_data: str, is_string: bool = True) -> str:
        if not is_string:
            raise NotImplementedError("Only string pingback data is currently supported")

        return hmac.new(
            self.gateway.config.private_key.encode(),
            pingback_data.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
