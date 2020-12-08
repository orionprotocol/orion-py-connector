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
""" print(client.getBalances()) """

""" Get Contract Balance for specific address """
""" print(client.getContractBalances()) """

""" Get Order History for Pair + Address """
""" print(client.getOrderHistory(
    "0xB0Fc7251682f639dcFc5beC6Dc86E30BA18Eb9fc", 'ORN-USDT'))
 """

""" Get Open Orders for Pair + Address """
""" print(client.getOpenOrders('ORN-USDT')) """


""" Prepare a test function before implementing the endpoints """
print(client.createOrder('ORN-USDT', True, 13.7477, 3.188061))

""" print(client.cancelOrder(173234)) """

""" print(client.cancelAllOrders()) """

""" 
print(client.getOrderbook('ORN-USDT')) """

""" client.cancelOrder() """
