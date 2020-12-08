from orion_py_connector.connector import Client

client = Client(
    'a284ec0d4b412f72c56f019acd9b9e580ce6fd6211c21e76f47b86413999834a')


def test_getBalances():
    balances = client.getBalances()
    assert balances != None


def test_getContractBalances():
    contractBalances = client.getContractBalances()
    assert contractBalances != None


def test_getOrderHistoryWithInvalidPair():
    orderHistory = client.getOrderHistory("ORN-LINK")
    assert orderHistory == None


def test_getOrderHistoryWithValidPair():
    orderHistory = client.getOrderHistory("ORN-USDT")
    assert orderHistory != None


def test_getOrderbookWithInvalidPair():
    orderbook = client.getOrderbook('ORN-LINK')
    assert len(orderbook['asks']) == 0 and len(orderbook['bids']) == 0


def test_getOrderbookWithValidPair():
    orderbook = client.getOrderbook('ORN-USDT')
    assert len(orderbook['asks']) > 0 and len(orderbook['bids']) > 0
