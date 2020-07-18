import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCoreSetupHandlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_state_unit(self):
        print('[ * ]: EWallet Client Core Setup Handlers')
        setup_handlers = self.core.setup_handlers(**{
            'handlers': ['action'],
            'actions': [
                'RequestClientID',
                'RequestSessionToken',
            ]
        })
        print(str(setup_handlers) + '\n')
        return setup_handlers
