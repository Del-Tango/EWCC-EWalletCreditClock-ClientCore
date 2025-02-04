import unittest

from ewcc_lib import ewallet_client

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionCheckSTokenLinked(unittest.TestCase):

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
        cls.core = ewallet_client.EWalletClientCore()

        print('[ + ] Prerequisits -')
        # Settups all action and event handlers
        print('[...] Subroutine Setup Handlers')
        cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CheckSTokenLinked'
            ]
        )
        print('[...] Subroutine Execute RequestClientId')
        cls.client_id = cls.core.execute('RequestClientID')

        print('[...] Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'RequestSessionToken', **{'client_id': cls.client_id.get('client_id')}
        )

        print('[...] Subroutine Execute RequestSessionToken')
        cls.session_token = cls.core.execute('RequestSessionToken')

        print('[...] Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'CheckSTokenLinked', **{
                'session_token': cls.session_token.get('session_token')
            }
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_execute_action_check_stoken_linked_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action CheckSTokenLinked -')
        execute = self.core.execute('CheckSTokenLinked')
        print(
            "[ I ]: core.execute('CheckSTokenLinked') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 4)
        self.assertTrue(isinstance(execute.get('client_id'), str))
        self.assertTrue(isinstance(execute.get('session_token'), str))
        self.assertTrue(isinstance(execute.get('linked'), bool))
        self.assertTrue(execute.get('linked'))
        return execute
