from fasterpay.config import Config
from fasterpay.signature import Signature
from fasterpay.pingback import Pingback
from fasterpay.paymentform import PaymentForm
from fasterpay.subscription import Subscription
from fasterpay.transaction import Transaction
from fasterpay.address import Address
from fasterpay.contact import Contact
from fasterpay.payout import Payout
from fasterpay.einvoice import EInvoice
class Gateway:
    def __init__(
        self,
        private_key: str,
        public_key: str,
        is_test: bool = False,
        api_version: str = "1.0.0",
    ):
        self.config = Config(
            private_key=private_key,
            public_key=public_key,
            is_test=is_test,
            api_version=api_version,
        )

    def payment_form(self) -> PaymentForm:
        return PaymentForm(self)

    def signature(self) -> Signature:
        return Signature(self)

    def pingback(self) -> Pingback:
        return Pingback(self)

    def get_config(self) -> Config:
        return self.config

    def subscription(self) -> Subscription:
        return Subscription(self)

    def transaction(self) -> Transaction:
        return Transaction(self)
    
    def address(self) -> Address:
        return Address(self)
    
    def contact(self) -> Contact:
        return Contact(self)
    
    def payout(self) -> Payout:
        return Payout(self)
    
    def einvoice(self) -> EInvoice:
        return EInvoice(self)
    