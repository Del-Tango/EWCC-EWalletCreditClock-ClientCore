import unittest
import os

from ewallet_client import EWalletClientCore

config_file = os.getcwd() + '/conf/ewcc.conf'


class TestEwalletClientExecuteActionRequestClientID(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_score = 'ewsc.systemcore@alvearesolutions.ro'

        cls.user1_name = 'EWCC-TestUser1Name'
        cls.user1_email = 'test1@ewcc.com'
        cls.user1_pass = '1234abcs!@#$'

        cls.user2_name = 'EWCC-TestUser2Name'
        cls.user2_email = 'test2@ewcc.com'
        cls.user2_pass = 'abcs!@#$1234'
        cls.user2_alias = 'TEWCCU2'

        cls.user3_name = 'EWCC-TestMaster3'
        cls.user3_email = 'master3@ewcc.com'
        cls.user3_pass = 'avsv!@#1234'
        cls.user3_alias = 'TEWCCM3'
        cls.user3_address = 'Jud.Iasi, Iasi, Str.Canta No.40'
        cls.user3_company = 'EWCC-TestCompany'

        cls.master_key_code = 'EWSC-Master-Key-Code'

        # Instantiate EWCC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

        print('[ + ] Prerequisits -')

        print('[...] Subroutine Setup Handlers')
        cls.core.setup_handlers(
            handlers=['action'], actions=['RequestClientID']
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_execute_action_request_client_id_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action RequestClientID -')
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
