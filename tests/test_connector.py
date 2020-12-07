from orion_py_connector.connector import Client

client = Client(
    'a284ec0d4b412f72c56f019acd9b9e580ce6fd6211c21e76f47b86413999834a')


def test_getBalancesWithInvalidAddress():
    balances = client.getBalances("")
    assert balances == None


def test_getBalancesWithValidAddress():
    balances = client.getBalances("0x1FF516E5ce789085CFF86d37fc27747dF852a80a")
    assert balances != None


def test_getContractBalancesWithInvalidAddress():
    contractBalances = client.getContractBalances("")
    assert contractBalances == None


def test_getContractBalancesWithValidAddress():
    contractBalances = client.getContractBalances(
        "0x1FF516E5ce789085CFF86d37fc27747dF852a80a")
    assert contractBalances != None


def test_getOrderHistoryWithInvalidAddressAndValidPair():
    orderHistory = client.getOrderHistory("", "ORN-USDT")
    assert len(orderHistory) == 0


def test_getOrderHistoryWithValidAddressButInvalidPair():
    orderHistory = client.getOrderHistory(
        "0x1FF516E5ce789085CFF86d37fc27747dF852a80a", "ORN-LINK")
    assert orderHistory == None


def test_getOrderHistoryWithValidAddressAndValidPair():
    orderHistory = client.getOrderHistory(
        "0x1FF516E5ce789085CFF86d37fc27747dF852a80a", "ORN-USDT")
    assert orderHistory != None


def test_getOrderbookWithInvalidPair():
    orderbook = client.getOrderbook('ORN-LINK')
    assert len(orderbook['asks']) == 0 and len(orderbook['bids']) == 0


def test_getOrderbookWithValidPair():
    orderbook = client.getOrderbook('ORN-USDT')
    assert len(orderbook['asks']) > 0 and len(orderbook['bids']) > 0
