VALID_PAIRS = ['ORN-USDT', 'ETH-USDT']
TOKENS = {
    "ETH": "0x0000000000000000000000000000000000000000",
    "USDT": "0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
    "ORN": "0xfc25454ac2db9f6ab36bc0b0b034b41061c00982"
}

PAIR_CONFIG = [
    {
        "name": "ETH-USDT",
        "minQty": 1.0E-5,
        "maxQty": 9000.0,
        "minPrice": 0.01,
        "maxPrice": 1000000.0,
        "pricePrecision": 2,
        "qtyPrecision": 5,
        "baseAssetPrecision": 8,
        "quoteAssetPrecision": 8,
        "limitOrderThreshold": 0.001
    },
    {
        "name": "ORN-USDT",
        "minQty": 1.0,
        "maxQty": 900000.0,
        "minPrice": 1.0E-4,
        "maxPrice": 1000.0,
        "pricePrecision": 4,
        "qtyPrecision": 0,
        "baseAssetPrecision": 8,
        "quoteAssetPrecision": 8,
        "limitOrderThreshold": 0.001
    },
    {
        "name": "LINK-USDT",
        "minQty": 0.01,
        "maxQty": 900000.0,
        "minPrice": 1.0E-4,
        "maxPrice": 1000.0,
        "pricePrecision": 4,
        "qtyPrecision": 2,
        "baseAssetPrecision": 8,
        "quoteAssetPrecision": 8,
        "limitOrderThreshold": 0.001
    },
    {
        "name": "BTMX-USDT",
        "minQty": 1.0,
        "maxQty": 900000.0,
        "minPrice": 1.0E-5,
        "maxPrice": 1000.0,
        "pricePrecision": 5,
        "qtyPrecision": 0,
        "baseAssetPrecision": 8,
        "quoteAssetPrecision": 8,
        "limitOrderThreshold": 0.001
    },
    {
        "name": "CTK-USDT",
        "minQty": 0.01,
        "maxQty": 900000.0,
        "minPrice": 1.0E-4,
        "maxPrice": 1000.0,
        "pricePrecision": 4,
        "qtyPrecision": 2,
        "baseAssetPrecision": 8,
        "quoteAssetPrecision": 8,
        "limitOrderThreshold": 0.001
    }
]


def getNumberFormat(pair: str):
    numberFormat = None
    for pairConfig in PAIR_CONFIG:
        if pairConfig['name'] == pair:
            numberFormat = pairConfig
    return numberFormat


def isValidPair(pair: str) -> bool:
    """ Check if pair is valid"""
    isValidPair = pair in VALID_PAIRS
    return isValidPair


def getAssetsFromPair(pair: str) -> list:
    arr = pair.split('-')
    if not len(arr) == 2:
        return None

    base = TOKENS.get(arr[0])
    quote = TOKENS.get(arr[1])
    if not base or not quote:
        return None

    return [base, quote]
