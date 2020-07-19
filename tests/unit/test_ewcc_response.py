import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)
        # Settups all action and event handlers
        cls.core.setup_handlers()
        cls.core.execute('RequestClientID')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_response_core_unit(self):
        print('[ * ]: EWallet Client Core Last Response Details -')
        response = self.core.last_response()
        print(
            "[ I ]: core.last_response() \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertFalse(response.get('failed'))
        self.assertEqual(len(response.keys()), 2)
        self.assertTrue(isinstance(response.get('response'), dict))
        self.assertEqual(len(response['response'].keys()), 5)
        self.assertTrue(isinstance(response['response'].get('execute'), str))
        self.assertTrue(isinstance(response['response'].get('action'), str))
        self.assertTrue(isinstance(response['response'].get('event'), str))
        self.assertTrue(isinstance(response['response'].get('instruction_set_response'), dict))
        return response
