import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionRequestSessionToken(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_score = 'ewsc.systemcore@alvearesolutions.ro'

        cls.user1_name = 'EWCC-TestUser1Name'
        cls.user1_email = 'test1@ewcc.com'
        cls.user1_pass = '1234abcs!@#$'

        cls.user2_name = 'EWCC-TestUser2Name'
        cls.user2_email = 'test2@ewcc.com'
        cls.user2_pass = 'abcs!@#$1234'

        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

        print('[ + ] Prerequisits -')
        # Settups all action and event handlers
        print('[...] Subroutine Setup Handlers')
        cls.core.setup_handlers(
            handlers=['action'],
            actions=['RequestClientID', 'RequestSessionToken']
        )
        print('[...] Subroutine Execute RequestClientId')
        cls.client_id = cls.core.execute('RequestClientID')

        print('[...] Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'RequestSessionToken', **{'client_id': cls.client_id.get('client_id')}
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_execute_action_request_client_id_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action RequestClientID -')
        execute = self.core.execute('RequestSessionToken')
        print(
            "[ I ]: core.execute('RequestSessionToken') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 2)
        self.assertTrue(isinstance(execute.get('session_token'), str))
        return execute
