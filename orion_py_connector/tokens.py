VALID_PAIRS = ['ORN-USDT', 'ETH-USDT']
TOKENS = {
    "ETH": "0x0000000000000000000000000000000000000000",
    "USDT": "0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
    "ORN": "0xfc25454ac2db9f6ab36bc0b0b034b41061c00982"
}


def isValidPair(pair: str) -> bool:
    """ Check if pair is valid"""
    isValidPair = pair in VALID_PAIRS
    return isValidPair


def getAssetsFromPair(pair: str) -> list:
    arr = pair.split('-')
    if not len(arr) == 2:
        return None
    base = TOKENS[arr[0]]
    if not len(base) > 0:
        return None
    quote = TOKENS[arr[1]]
    if not len(quote) > 0:
        return None

    return [base, quote]
