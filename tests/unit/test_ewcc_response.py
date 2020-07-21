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

    def test_ewcc_response_core_raw_unit(self):
        print('[ * ]: EWallet Client Core Raw Last Response -')
        response = self.core.last_response(raw=True)
        print(
            "[ I ]: core.last_response(raw=True) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(response)
        return response

    def test_ewcc_response_core_execution_unit(self):
        print('[ * ]: EWallet Client Core Execution Last Response -')
        response = self.core.last_response(raw=False)
        print(
            "[ I ]: core.last_response(raw=False) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(len(response), 2)
        self.assertFalse(response.get('failed'))
        return response

    def test_ewcc_response_action_request_client_id_unit(self):
        print('[ * ]: EWallet Client Core Action Last Response -')
        response = self.core.last_response('RequestClientID')
        print(
            "[ I ]: core.last_response('RequestClientID') \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(len(response), 2)
        self.assertFalse(response.get('failed'))
        return response

    def test_ewcc_response_specific_action_request_client_id_unit(self):
        print('[ * ]: EWallet Client Core Specific Action Last Response -')
        response = self.core.actions['RequestClientID'].last_response()
        print(
            "[ I ]: core.actions['RequestClientID'].last_response() \n"
            "[ I ]: core.actions['RequestClientID'].last_response(raw=False) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertEqual(len(response), 2)
        self.assertFalse(response.get('failed'))
        return response

    def test_ewcc_response_specific_raw_action_request_client_id_unit(self):
        print('[ * ]: EWallet Client Core Specific Action Last Response Raw -')
        response = self.core.actions['RequestClientID'].last_response(raw=True)
        print(
            "[ I ]: core.actions['RequestClientID'].last_response(raw=True) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(response)
        return response
