from web3.auto import w3
from eth_account.messages import SignableMessage, HexBytes
from eth_account import Account
from eip712_structs import EIP712Struct, make_domain, Address, String, Uint, Bytes
import logging
import math

logging.getLogger('orion_py_connector.utils').addHandler(
    logging.NullHandler())

EIP712_DOMAIN = make_domain(name="Orion Exchange", version="1", chainId=3,
                            salt="0xf2d857f4a3edcb9b78b4d503bfe733db1e3f6cdc2b7971ee739626c97e86a557")
MATCHER_ADDRESS = '0x1FF516E5ce789085CFF86d37fc27747dF852a80a'
MATCHER_FEE_PERCENT = 0.002
DEFAULT_EXPIRATION = 29 * 24 * 60 * 60 * 1000


class Order(EIP712Struct):
    """ Order Struct according to the EIP-712 Standard """
    senderAddress = Address()
    matcherAddress = Address()
    baseAsset = Address()
    quoteAsset = Address()
    matcherFeeAsset = Address()
    amount = Uint(64)
    price = Uint(64)
    matcherFee = Uint(64)
    nonce = Uint(64)
    expiration = Uint(64)
    buySide = Uint(8)


class DeleteOrder(EIP712Struct):
    senderAddress = Address()
    id = Uint(64)


def isValidAddress(address: str) -> bool:
    logging.debug(f'Calling isValidAddress with args: {address}')
    isValidAddress = w3.isAddress(address)
    return isValidAddress


def signEIP712Struct(data: EIP712Struct, private_key: str) -> str:
    logging.debug(f'Calling signEIP712Struct with args: {data.data_dict()}')
    message = data.signable_bytes(EIP712_DOMAIN)
    sm = SignableMessage(
        HexBytes(b'\x01'),
        message[2: 34],
        message[34: 66]
    )

    account = Account.from_key(private_key)
    signed = Account.sign_message(sm, account.key)
    new_addr = Account.recover_message(sm, signature=signed.signature)
    assert new_addr == account.address

    signature = signed.signature.hex()
    logging.info(f'Order Signature: {signature}')
    return signature


def hashOrder(data: Order) -> str:
    logging.debug(f'Calling hashOrder with args: {data.data_dict()}')
    buySide = '0x00' if data.get_data_value('buySide') == 0 else '0x01'
    hash = w3.solidityKeccak(
        [
            'bytes32',
            'address',
            'address',
            'address',
            'address',
            'address',
            'uint64',
            'uint64',
            'uint64',
            'uint64',
            'uint64',
            'bytes32'
        ], [
            '0x03',
            w3.toChecksumAddress(data.get_data_value('senderAddress')),
            w3.toChecksumAddress(data.get_data_value('matcherAddress')),
            w3.toChecksumAddress(data.get_data_value('baseAsset')),
            w3.toChecksumAddress(data.get_data_value('quoteAsset')),
            w3.toChecksumAddress(data.get_data_value('matcherFeeAsset')),
            data.get_data_value('amount'),
            data.get_data_value('price'),
            data.get_data_value('matcherFee'),
            data.get_data_value('nonce'),
            data.get_data_value('expiration'),
            buySide
        ]).hex()
    logging.info(f'Order Hash: {hash}')
    return hash


def toBaseUnit(amount: float, decimals: int = 8) -> int:
    return int(amount * 10 ** decimals)
