import logging
from web3.auto import w3
from json import dumps
import time
import warnings
import requests
from orion_py_connector.tokens import VALID_PAIRS, isValidPair, getAssetsFromPair
from orion_py_connector.utils import (DEFAULT_EXPIRATION, MATCHER_ADDRESS, MATCHER_FEE_PERCENT,
                                      isValidAddress, signEIP712Struct, hashOrder, toBaseUnit, Order, DeleteOrder)

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

    def getBalances(self, address: str):
        logging.debug(f'Calling getBalances with args: {address}')
        isValidAddress(address)

        url = f'{self.broker_url}/getBalance/{address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getContractBalances(self, address: str):
        logging.debug(f'Calling getContractBalances with args: {address}')
        isValidAddress(address)

        url = f'{self.broker_url}/getContractBalance/{address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getOrderHistory(self, address: str, pair: str):
        logging.debug(f'Calling getOrderHistory with args: {address}, {pair}')
        isValidAddress(address)
        isValidPair(pair)

        url = f'{self.backend_url}/orderHistory'
        params = {'symbol': pair, 'address': address}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def getOpenOrders(self, address: str, pair: str):
        logging.debug(f'Calling getOpenOrders with args: {address}, {pair}')
        isValidAddress(address)
        isValidPair(pair)

        history = self.getOrderHistory(address, pair)
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

    def cancelOrder(self, address: str, id: int) -> bool:
        logging.debug(f'Calling cancelOrder with args: {address}, {id}')
        cancelOrder = DeleteOrder(senderAddress=address, id=id)
        signature = signEIP712Struct(cancelOrder, self.private_key)

        payload = cancelOrder.data_dict()
        payload['signature'] = signature

        print(payload)
        url = f'{self.backend_url}/order'
        response = requests.request('delete',
                                    url, json=dumps(payload), headers=headers)

        return response.status_code == 200

    def cancelAllOrders(self, address: str):
        logging.debug(f'Calling cancelAllOrders with args: {address}')
        isValidAddress(address)

        allOrderCanceled = True

        for pair in VALID_PAIRS:
            openOrders = self.getOpenOrders(address, pair)
            for order in openOrders:
                if order['id'] > 0:
                    success = self.cancelOrder(address, order['id'])
                    if not success:
                        allOrderCanceled = False
        return allOrderCanceled

    def createOrder(self, address: str, pair: str, buy: bool, amount: int, price: int):
        logging.debug(
            f'Calling createOrder with args: {address}, {pair}, {buy}')
        isValidAddress(address)
        isValidPair(pair)

        assets = getAssetsFromPair(pair)
        matcherFeeAsset = assets[0] if buy else assets[1]
        matcherFee = amount * MATCHER_FEE_PERCENT if buy else amount * \
            price * MATCHER_FEE_PERCENT

        currentTimestamp = int(time.time()*1000)

        order = Order(senderAddress=address,
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

        if response.status_code == 200:
            return response.json()
        return None
