from fasterpay.gateway import Gateway
from random import randint

if __name__ == "__main__":

    gateway = Gateway("<Your Private key>", "<Your Public key>", True)

    response = gateway.subscription().cancel(order_id=7923)

    print (response)
