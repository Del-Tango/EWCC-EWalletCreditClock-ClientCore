import unittest

from ewcc_lib import ewallet_client


class TestEwalletClientResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()
        # Settups all action and event handlers
        cls.core.setup_handlers()
        cls.core.execute('RequestClientID')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_response_core_unit(self):
        print('[ * ]: EWCC Subroutine LastResponse Action-')
        self.core.execute('RequestClientID')
        response = self.core.last_response()
        print(
            "[ I ]: core.last_response() \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertFalse(response.get('failed'))
        self.assertEqual(len(response.keys()), 5)
        self.assertTrue(isinstance(response.get('execute'), str))
        self.assertTrue(isinstance(response.get('action'), str))
#       self.assertTrue(isinstance(response.get('event'), str))
        self.assertTrue(isinstance(response.get('instruction_set_response'), dict))
        return response

    def test_ewcc_response_core_raw_unit(self):
        print('[ * ]: EWCC Subroutine RawLastResponse -')
        response = self.core.last_response(raw=True)
        print(
            "[ I ]: core.last_response(raw=True) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(response)
        return response

    def test_ewcc_response_core_execution_unit(self):
        print('[ * ]: EWCC Subroutine ExecutionLastResponse -')
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
        print('[ * ]: EWCC Subroutine SpecificActionLastResponse -')
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
        print('[ * ]: EWCC Subroutine SpecificActionLastResponse -')
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
        print('[ * ]: EWCC Subroutine SpecificActionRawLastResponse -')
        response = self.core.actions['RequestClientID'].last_response(raw=True)
        print(
            "[ I ]: core.actions['RequestClientID'].last_response(raw=True) \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(response)
        return response
