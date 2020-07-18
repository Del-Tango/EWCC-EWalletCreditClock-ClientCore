import os
import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'

class TestEwalletClientCoreConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_user_request_client_id_functionality(self):
        print('[ * ]: EWallet Client Core Config')
        config = self.core.state()
        print(str(config) + '\n')
        return config



