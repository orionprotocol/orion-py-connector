from orion_py_connector.utils import hashOrder, isValidAddress, signEIP712Struct, Order
import pytest


def test_isInvalidAddress():
    isValid = isValidAddress(
        '0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9f')
    assert isValid == False


def test_isValidAddress():
    isValid = isValidAddress(
        '0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc')
    assert isValid


def test_hashOrder():
    order = Order(senderAddress="0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc",
                  matcherAddress="0x1FF516E5ce789085CFF86d37fc27747dF852a80a",
                  baseAsset="0x0000000000000000000000000000000000000000",
                  quoteAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                  matcherFeeAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                  amount=4990000,
                  price=58678000000,
                  matcherFee=5856064,
                  nonce=1607174399438,
                  expiration=1609679999438,
                  buySide=0
                  )
    id = hashOrder(order)
    expected_id = "0x0402bccc3cd8d3c7ec308743b0ac26510a5302b63e7b15901883509ff10a9942"
    assert id == expected_id


def test_signEIP712Struct():
    order = Order(senderAddress="0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc",
                  matcherAddress="0x1FF516E5ce789085CFF86d37fc27747dF852a80a",
                  baseAsset="0x0000000000000000000000000000000000000000",
                  quoteAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                  matcherFeeAsset="0xfc1cd13a7f126efd823e373c4086f69beb8611c2",
                  amount=4990000,
                  price=58678000000,
                  matcherFee=5856064,
                  nonce=1607174399438,
                  expiration=1609679999438,
                  buySide=0
                  )

    signature = signEIP712Struct(
        order, 'a284ec0d4b412f72c56f019acd9b9e580ce6fd6211c21e76f47b86413999834a')
    expected_signature = "0x64a05b918125de2c1cc45b1e004b81028c7767b23c65d21a832976ec4e08d274171f3c74045a20891d7a3709ccd2cc0d9681fdcaaa7bd7a9f24aa39c361e13bf1c"

    assert signature == expected_signature
