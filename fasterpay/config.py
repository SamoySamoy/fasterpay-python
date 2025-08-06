class Config:
    def __init__(
        self,
        private_key: str,
        public_key: str,
        is_test: bool = False,
        api_version: str = "1.0.0",
    ):
        self._private_key = private_key
        self._public_key = public_key
        self._api_base_url = (
            "https://pay.sandbox.fasterpay.com"
            if is_test else
            "https://pay.fasterpay.com"
        )
        self._api_version = api_version

    @property
    def public_key(self) -> str:
        return self._public_key

    @property
    def private_key(self) -> str:
        return self._private_key

    @property
    def api_url(self) -> str:
        return self._api_base_url

    @property
    def api_version(self) -> str:
        return self._api_version
