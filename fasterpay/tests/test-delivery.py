#!/usr/bin/bash

from fasterpay.gateway import Gateway

if __name__ == "__main__":

    # Initialize the Gateway
    gateway = Gateway("<YOUR PRIVATE KEY>", "<YOUR PUBLIC KEY>", True)

    # Prepare Delivery Information
    deliveryInfo = {
        "payment_order_id": "46157868",
        "merchant_order_id": "1078972173",
        "type": "digital",
        "public_key": gateway.get_config().get_public_key(),
        "status": "order_placed",
        "refundable": 1,
        "details": "Order placed today",
        "shipping_address[email]": "jon.doe@example.com"
    }

    deliverResponse = gateway.transaction().deliver(deliveryInfo)

    print(deliverResponse)
