""" Temporay test file before writing proper tests """

from orion_connector import connector

""" Create API connector """
client = connector.APIService(
    'a284ec0d4b412f72c56f019acd9b9e580ce6fd6211c21e76f47b86413999834a')

""" Get Balance for specific address """
""" print(client.get_balance("0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """

""" Get Contract Balance for specific address """
""" print(client.get_contract_balance("0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """

""" Get Order History for Pair + Address """
""" print(client.get_order_history('ORN-USDT',
                               "0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """

""" Get Open Orders for Pair + Address """
""" print(client.get_open_orders('ORN-USDT',
                             "0x1FF516E5ce789085CFF86d37fc27747dF852a80a")) """


""" Prepare a test function before implementing the endpoints """
client.test_sign()
