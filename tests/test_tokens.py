from orion_py_connector.tokens import getAssetsFromPair, isValidPair, TOKENS


def test_getAssetsFromValidPair():
    assets = getAssetsFromPair('ORN-USDT')
    assert assets == [TOKENS['ORN'], TOKENS['USDT']]


def test_getAssetsFromInvalidPair():
    assets = getAssetsFromPair('ORN-XRP')
    assert assets == None


def test_isInvalidPair():
    isValid = isValidPair('ORN-XRP')
    assert isValid == False


def test_isValidPair():
    isValid = isValidPair('ORN-USDT')
    assert isValid
