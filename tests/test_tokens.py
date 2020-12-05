from orion_py_connector.tokens import getAssetsFromPair, isValidPair, TOKENS


def getAssetsFromValidPair():
    assets = getAssetsFromPair('ORN-USDT')
    assert assets == [TOKENS['ORN'], TOKENS['USDT']]


def getAssetsFromInvalidPair():
    assets = getAssetsFromPair('ORN-ERD')
    assert assets == None


def test_isInvalidPair():
    isValid = isValidPair('ORN-ERD')
    assert isValid == False


def test_isVaidPair():
    isValid = isValidPair('ORN-USDT')
    assert isValid
