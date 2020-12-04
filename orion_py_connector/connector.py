from orion_py_connector.orderbook import Orderbook
from orion_py_connector.utils import isValidAddress, isValidPair
import requests
import warnings
from eip712_structs import make_domain, EIP712Struct, Address, String, Uint, Bytes
from web3.auto import w3
from eth_account.messages import SignableMessage, HexBytes
from eth_account import Account


class Order(EIP712Struct):
    """ Order Struct according to the EIP-712 Standard """
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


class Client:
    def __init__(self,
                 private_key: str,
                 broker_url: str = "https://stage.orionprotocol.io/api/broker",
                 backend_url: str = "https://stage.orionprotocol.io/backend/api/v1"):

        if len(private_key) == 0:
            raise Exception('You need to specify a private key')

        self.private_key = private_key
        self.broker_url = broker_url
        self.backend_url = backend_url
        self.orderbook = Orderbook()

    def getBalances(self, address: str):
        isValidAddress(address)

        url = f'{self.broker_url}/getBalance/{address}'
        result = requests.get(url)
        return result.json()

    def getContractBalances(self, address: str):
        isValidAddress(address)

        url = f'{self.broker_url}/getContractBalance/{address}'
        result = requests.get(url)
        return result.json()

    def getOrderHistory(self, address: str, pair: str):
        isValidAddress(address)
        isValidPair(pair)

        url = f'{self.backend_url}/orderHistory'
        params = {'symbol': pair, 'address': address}
        result = requests.get(url, params)
        return result.json()

    def getOpenOrders(self, address: str, pair: str):
        isValidAddress(address)
        isValidPair(pair)

        history = self.getOrderHistory(pair, address)
        open_orders = list(filter(lambda x: x['status'] == "OPEN", history))
        return open_orders

    def getOrderbook(self, pair: str):
        isValidPair(pair)

    def test_sign(self):

        my_domain = make_domain(name="Orion Exchange", version="1", chainId=3,
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
        message = order.signable_bytes(my_domain)
        sm = SignableMessage(
            HexBytes(b'\x01'),
            message[2: 34],
            message[34: 66]
        )

        account = Account.from_key(self.private_key)
        signed = Account.sign_message(sm, account.key)
        new_addr = Account.recover_message(sm, signature=signed.signature)
        assert new_addr == account.address

        signature = signed.signature.hex()
        expected_signature = "0x6c03305cfec161bd4589853993ef6051edd8babbcb094f1031d5df891c03c6e46912d4903669449030bb0e71c08b77b8e7a9a18b4a13e75a7bbbbdf21d1ea0831c"

        print(signature)
        print(expected_signature)
        print(signature == expected_signature)
        return None
