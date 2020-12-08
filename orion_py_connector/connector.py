import logging
from web3.auto import w3
from json import dumps
import time
import warnings
import requests
from eth_account import Account
from orion_py_connector.tokens import VALID_PAIRS, isValidPair, getAssetsFromPair, getNumberFormat
from orion_py_connector.utils import (DEFAULT_EXPIRATION, MATCHER_ADDRESS, MATCHER_FEE_PERCENT,
                                      signEIP712Struct, hashOrder, toBaseUnit, Order, DeleteOrder)

logging.getLogger('orion_py_connector.connector').addHandler(
    logging.NullHandler())

headers = {'content-type': 'application/json'}


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
        self.address = account = Account.from_key(private_key).address

    def getBalances(self):
        logging.debug(f'Calling getBalances')
        url = f'{self.broker_url}/getBalance/{self.address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getContractBalances(self):
        logging.debug(f'Calling getContractBalances')

        url = f'{self.broker_url}/getContractBalance/{self.address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getOrderHistory(self, pair: str):
        logging.debug(f'Calling getOrderHistory with args: {pair}')
        isValidPair(pair)

        url = f'{self.backend_url}/orderHistory'
        params = {'symbol': pair, 'address': self.address}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def getOpenOrders(self, pair: str):
        logging.debug(f'Calling getOpenOrders with args: {pair}')
        isValidPair(pair)

        history = self.getOrderHistory(pair)
        if history == None:
            return None
        open_orders = list(filter(lambda x: x['status'] == "OPEN", history))
        return open_orders

    def getOrderbook(self, pair: str, depth: int = 20):
        logging.debug(f'Calling getOrderbook with args: {pair}, {depth}')
        isValidPair(pair)

        url = f'{self.backend_url}/orderbook'
        params = {'pair': pair, 'depth': depth}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def cancelOrder(self, id: int) -> bool:
        logging.debug(f'Calling cancelOrder with args: {id}')
        cancelOrder = DeleteOrder(senderAddress=self.address, id=id)
        signature = signEIP712Struct(cancelOrder, self.private_key)

        payload = cancelOrder.data_dict()
        payload['signature'] = signature

        print(payload)
        url = f'{self.backend_url}/order'
        response = requests.request('delete',
                                    url, json=dumps(payload), headers=headers)

        return response.status_code == 200

    def cancelAllOrders(self):
        logging.debug(f'Calling cancelAllOrders')

        allOrderCanceled = True

        for pair in VALID_PAIRS:
            openOrders = self.getOpenOrders(pair)
            for order in openOrders:
                if order['id'] > 0:
                    success = self.cancelOrder(order['id'])
                    if not success:
                        allOrderCanceled = False
        return allOrderCanceled

    def createOrder(self, pair: str, buy: bool, amount: float, price: float):
        logging.debug(
            f'Calling createOrder with args: {pair}, {buy}')
        isValidPair(pair)

        numberFormat = getNumberFormat(pair)

        assets = getAssetsFromPair(pair)
        amount = round(amount, numberFormat['qtyPrecision'])
        price = round(price, numberFormat['pricePrecision'])
        matcherFeeAsset = assets[0] if buy else assets[1]
        matcherFee = amount * MATCHER_FEE_PERCENT if buy else amount * \
            price * MATCHER_FEE_PERCENT

        currentTimestamp = int(time.time()*1000)

        order = Order(senderAddress=self.address,
                      matcherAddress=MATCHER_ADDRESS,
                      baseAsset=assets[0],
                      quoteAsset=assets[1],
                      matcherFeeAsset=matcherFeeAsset,
                      amount=toBaseUnit(amount),
                      price=toBaseUnit(price),
                      matcherFee=toBaseUnit(matcherFee),
                      nonce=currentTimestamp,
                      expiration=currentTimestamp+DEFAULT_EXPIRATION,
                      buySide=1 if buy else 0
                      )

        payload = order.data_dict()
        payload['id'] = hashOrder(order)
        payload['signature'] = signEIP712Struct(order, self.private_key)

        logging.info(f'Order: {payload}')

        url = f'{self.backend_url}/order'
        response = requests.post(
            url, dumps(payload), headers=headers)

        print(response.json())
        if response.status_code == 200:
            return response.json()
        return None
