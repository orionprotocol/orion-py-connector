""" Temporay test file before writing proper tests """

from orion_py_connector import connector
from orion_py_connector.tokens import getAssetsFromPair
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

""" Create API connector """
client = connector.Client(
    'a284ec0d4b412f72c56f019acd9b9e580ce6fd6211c21e76f47b86413999834a')

""" Get Balance for specific address """
""" print(client.getBalances("0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """

""" Get Contract Balance for specific address """
""" print(client.getContractBalances("0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """

""" Get Order History for Pair + Address """
""" print(client.getOrderHistory(
    "0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc", 'ORN-USDT'))
 """

""" Get Open Orders for Pair + Address """
""" print(client.getOpenOrders("0x1FF516E5ce789085CFF86d37fc27747dF852a80a", 'ORN-USDT')) """


""" Prepare a test function before implementing the endpoints """
print(client.createOrder(
    "0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc", 'ORN-USDT', True, 13.7477, 3.188061))

""" print(client.cancelOrder(
    '0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc', 173234)) """

""" print(client.cancelAllOrders(
    '0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc')) """

""" 
print(client.getOrderbook('ORN-USDT')) """

""" client.cancelOrder() """
