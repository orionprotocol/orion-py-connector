import requests
from eip712_structs import make_domain, EIP712Struct, Address, String, Uint
from web3.auto import w3
from eth_account.messages import encode_defunct

""" Order Struct according to the EIP-712 Standard """


class Order(EIP712Struct):
    senderAddress = Address()
    matcherAddress = Address()
    baseAsset = Address()
    quoteAsset = Address()
    matcherFeeAsset = Address()
    amount = Uint(64)
    price = Uint(64)
    matcherFee = Uint(64)
    nonce = Uint(64)
    expiration = Uint(64)
    buySide = Uint(8)


class APIService:
    def __init__(self,
                 private_key,
                 broker_url="https://stage.orionprotocol.io/api/broker",
                 backend_url="https://stage.orionprotocol.io/backend/api/v1"):

        self.private_key = private_key
        self.broker_url = broker_url
        self.backend_url = backend_url

    def get_balance(self, address):
        url = f'{self.broker_url}/getBalance/{address}'
        result = requests.get(url)
        return result.json()

    def get_contract_balance(self, address):
        url = f'{self.broker_url}/getContractBalance/{address}'
        result = requests.get(url)
        return result.json()

    def get_order_history(self, pair, address):
        url = f'{self.backend_url}/orderHistory'
        params = {'symbol': pair, 'address': address}
        result = requests.get(url, params)
        return result.json()

    def get_open_orders(self, pair, address):
        history = self.get_order_history(pair, address)
        open_orders = list(filter(lambda x: x['status'] == "OPEN", history))
        return open_orders

    def test_sign(self):
        domain = make_domain(name="Orion Exchange", version="1", chainId=3,
                             salt="0xf2d857f4a3edcb9b78b4d503bfe733db1e3f6cdc2b7971ee739626c97e86a557")

        order = Order(senderAddress="0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc",
                      matcherAddress="0x1FF516E5ce789085CFF86d37fc27747dF852a80a",
                      baseAsset="0x0000000000000000000000000000000000000000",
                      quoteAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                      matcherFeeAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                      amount=19960000,
                      price=61879000000,
                      matcherFee=24827388,
                      nonce=1607011557478,
                      expiration=1609517157478,
                      buySide=0
                      )

        message = order.signable_bytes(domain)
        message = encode_defunct(primitive=message)
        signed_message = w3.eth.account.sign_message(
            message, private_key=self.private_key)

        signature = signed_message.signature.hex()
        expected_signature = "0x6c03305cfec161bd4589853993ef6051edd8babbcb094f1031d5df891c03c6e46912d4903669449030bb0e71c08b77b8e7a9a18b4a13e75a7bbbbdf21d1ea0831c"

        print(signature)
        print(expected_signature)
        print(signature == expected_signature)
        return None
