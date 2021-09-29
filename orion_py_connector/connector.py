import logging
from json import dumps
import time
import requests
from eth_account import Account
from orion_py_connector.utils import (DEFAULT_EXPIRATION,
                                      signEIP712Struct, hashOrder, toBaseUnit, Order, DeleteOrder)

logging.getLogger('orion_py_connector.connector').addHandler(
    logging.NullHandler())

headers = {'content-type': 'application/json'}


OPEN_STATUS = ["NEW", "ACCEPTED", "ROUTING", "PARTIALLY_FILLED", "TX_PENDING"]
FILL_ORDERS_GAS_LIMIT_FOR_FEE_CALCULATION = 220000
BASE_ASSET = "0x0000000000000000000000000000000000000000"
PLATFORM_PERCENT = 0.002 #0.2%

class Client:
    def __init__(self,
                 private_key: str,
                 api_url: str = "https://staging.orionprotocol.io/api",
                 backend_url: str = "https://staging.orionprotocol.io/backend/api/v1"):

        if len(private_key) == 0:
            raise Exception('You need to specify a private key')

        self.private_key = private_key
        self.api_url = api_url
        self.backend_url = backend_url
        self.address = account = Account.from_key(private_key).address
        self.default_orn_fee = 3
        self.loadInfo()

    def loadInfo(self):
        logging.debug(f'Loading Info')
        url = f'{self.api_url}/info'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Couldn't load API Info")
        info = response.json()
        self.TOKENS = info['assetToAddress']
        self.orn_address = self.TOKENS['ORN']
        self.chain_id = info['chainId']
        self.matcher_address = info['matcherAddress']
        return None

    def getAssetsFromPair(self, pair: str) -> list:
        arr = pair.split('-')
        if not len(arr) == 2:
            return None

        base = self.TOKENS.get(arr[0])
        quote = self.TOKENS.get(arr[1])
        if not base or not quote:
            return None

        return [base, quote]

    def splitPair(self, pair: str) -> list:
        arr = pair.split('-')
        if not len(arr) == 2:
            return None

        return [arr[0], arr[1]]

    def getBalances(self):
        logging.debug(f'Calling getBalances')
        url = f'{self.api_url}/broker/getBalance/{self.address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getContractBalances(self):
        logging.debug(f'Calling getContractBalances')

        url = f'{self.api_url}/broker/getContractBalance/{self.address}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def getReservedBalances(self):
        logging.debug(f'Calling getReservedBalances')

        url = f'{self.backend_url}/address/balance/reserved?address={self.address}'
        response = requests.get(url)
        if response.status_code == 200:
            bal = response.json()
            return {k.upper(): v for k, v in bal.items()}
        return None

    def getAvailableBalances(self):
        logging.debug(f'Calling getAvailableBalances')

        balance = self.getContractBalances()
        reserved = self.getReservedBalances()

        for r in reserved:
            if r in balance:
                balance[r] = str(round(float(balance[r]) - float(reserved[r]), 8))

        return balance

    def getOrderHistory(self, pair: str):
        logging.debug(f'Calling getOrderHistory with args: {pair}')

        url = f'{self.backend_url}/order/history'
        [baseAsset, quoteAsset] = self.splitPair(pair)
        params = {'baseAsset': baseAsset, 'quoteAsset': quoteAsset, 'address': self.address}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def getOpenOrders(self, pair: str):
        logging.debug(f'Calling getOpenOrders with args: {pair}')

        history = self.getOrderHistory(pair)
        if history == None:
            return []
        open_orders = list(
            filter(lambda x: x['status'] in OPEN_STATUS, history))
        return open_orders

    def getOrderbook(self, pair: str, depth: int = 20):
        logging.debug(f'Calling getOrderbook with args: {pair}, {depth}')

        url = f'{self.backend_url}/orderbook/'
        params = {'pair': pair, 'depth': depth}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def getOrderbookExchange(self, pair: str, exchange:str, depth: int = 20):
        logging.debug(f'Calling getOrderbook with args: {pair}, {depth}')

        url = f'{self.backend_url}/orderbook/{exchange}/{pair}'
        params = {'filterByBrokerBalances': True, 'depth': depth}
        response = requests.get(url, params)
        if response.status_code == 200:
            return response.json()
        return None

    def getOrderInfo(self, orderId: int):
        logging.debug(f'Calling getOrderInfo with args: {orderId}')

        url = f'{self.backend_url}/order'
        params = {'orderId': orderId}
        response = requests.get(url, params)

        if response.status_code == 200:
            return response.json()
        return None

    def cancelOrder(self, id: str) -> bool:
        logging.debug(f'Calling cancelOrder with args: {id}')
        cancelOrder = DeleteOrder(sender=self.address, id=id, isPersonalSign=True)
        signature = signEIP712Struct(self.chain_id, cancelOrder, self.private_key)

        payload = {'id': id, 'sender': self.address, 'signature': signature, 'isPersonalSign': True}

        url = f'{self.backend_url}/order'
        response = requests.delete(url, data=dumps(payload), headers=headers)

        return response.status_code == 200

    def cancelAllOrders(self, pair: str):
        logging.debug(f'Calling cancelAllOrders')

        allOrderCanceled = True

        for order in self.getOpenOrders(pair):
            if order['id']:
                success = self.cancelOrder(order['id'])
                if not success:
                    allOrderCanceled = False

        return allOrderCanceled

    def getNetworkFeeInOrn(self):
        logging.debug(f'Loading Gas Price')
        url = f'{self.api_url}/gasPrice'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Couldn't load Gas Price")
        gasPrice = float(response.text.replace('"', ''))
        return FILL_ORDERS_GAS_LIMIT_FOR_FEE_CALCULATION*gasPrice*self.getPriceByToken(BASE_ASSET)/1e18

    def getPriceByToken(self, token) -> float:
        logging.debug(f'Loading Prices')
        url = f'{self.api_url}/prices'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Couldn't load Prices")

        prices = response.json()
        return float(prices[token])

    def getPrice(self, asset) -> float:
        return self.getPriceByToken(self.TOKENS.get(asset))

    def getOrderFeeInOrn(self, amount: float, baseAsset: str) -> float:
        return round(self.getPrice(baseAsset)*amount*PLATFORM_PERCENT + self.getNetworkFeeInOrn(), 8)

    def createOrder(self, pair: str, buy: bool, amount: float, price: float, fee: float=None, makerOnly=False):
        if fee is None:
            [baseCur, _] = self.splitPair(pair)
            fee = self.getOrderFeeInOrn(amount, baseCur)

        logging.debug(
            f'Calling createOrder with args: {pair}, {buy}')

        assets = self.getAssetsFromPair(pair)
        matcherFeeAsset = self.orn_address
        matcherFee = fee

        currentTimestamp = int(time.time()*1000)

        order = Order(senderAddress=self.address,
                      matcherAddress=self.matcher_address,
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
        payload['signature'] = signEIP712Struct(self.chain_id, order, self.private_key)

        logging.info(f'Order: {payload}')

        url = f'{self.backend_url}/order' + ('/internal' if makerOnly else '')
        response = requests.post(
            url, dumps(payload), headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f'Failed to create order: {response.text}')
        return None

    def getMarketPrice(self, assetIn: str, amountIn: float, assetOut: str):
        logging.debug(f'Loading market price for {amountIn} {assetIn} in {assetOut}')
        url = f'{self.backend_url}/swap?amountIn={amountIn}&assetIn={assetIn}&assetOut={assetOut}'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Couldn't load market price")

        res = response.json()

        logging.debug(f'Got swap: {res}')

        order_info = res['orderInfo']

        side = order_info['side']
        amount_out = res['amountOut']
        available_amount_in = res['availableAmountIn']

        # amount_out / available_amount_in if(side == 'SELL') else available_amount_in / amount_out
        price = res['marketPrice'] if(side == 'SELL') else 1 / res['marketPrice']

        result = {
            'price': price,
            'safePrice': order_info['safePrice'],
            'isPool': res['isThroughPoolOptimal'],
            'availableQty': available_amount_in,
            'qtyOut': amount_out,
            'side': side,
        }

        logging.info(f'Got market price {result}')

        return result
