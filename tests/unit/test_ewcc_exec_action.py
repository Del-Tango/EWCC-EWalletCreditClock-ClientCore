import unittest

from ewcc_lib import ewallet_client

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()
        # Settups all action and event handlers
        cls.core.setup_handlers()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_execute_action_request_client_id_unit(self):
        print('[ * ]: EWCC Subroutine Execute ActionRequestClientID -')
        execute = self.core.execute('RequestClientID')
        print(
            "[ I ]: core.execute('RequestClientID') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 2)
        self.assertTrue(isinstance(execute.get('client_id'), str))
        return execute
