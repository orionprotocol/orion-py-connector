from web3.auto import w3

VALID_PAIRS = ['ORN-USDT', 'ETH-USDT']


def isValidAddress(address: str, throwException: bool = True):
    """ Check if address is valid """
    isValidAddress = w3.isAddress(address)
    if not isValidAddress and throwException:
        raise Exception('Invalid address specified')
    return isValidAddress


def isValidPair(pair: str, throwException: bool = True):
    """ Check if pair is valid"""
    isValidPair = pair in VALID_PAIRS
    if not isValidPair and throwException:
        raise Exception('Invalid pair specified')
    return isValidPair
