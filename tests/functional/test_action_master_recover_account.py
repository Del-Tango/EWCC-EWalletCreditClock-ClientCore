import unittest
import pysnooper

from ewcc_lib import ewallet_client

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionMasterRecoverAccount(unittest.TestCase):

    @classmethod
#   @pysnooper.snoop()
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
        cls.core = ewallet_client.EWalletClientCore()

        print('[ + ]: Prerequisits -')

        print('[...]: Subroutine Setup Handlers')
        setup_handlers = cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateMaster',
                'MasterAccountLogin', 'MasterUnlinkAccount',
                'MasterRecoverAccount',
            ]
        )
        print('[...]: Subroutine Execute RequestClientId')
        client_id = cls.core.execute('RequestClientID')
        cls.client_id = client_id

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'RequestSessionToken',
            **{
                'client_id': cls.client_id.get('client_id')
            }
        )
        print('[...]: Subroutine Execute RequestSessionToken')
        session_token = cls.core.execute('RequestSessionToken')
        cls.session_token = session_token

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'CreateMaster',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': cls.user3_name,
                'user_email': cls.user3_email,
                'user_pass': cls.user3_pass,
                'user_alias': cls.user3_alias,
                'company': cls.user3_company,
                'address': cls.user3_address,
            }
        )
        print('[...]: Subroutine Execute CreateMaster')
        create_master = cls.core.execute('CreateMaster')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'MasterAccountLogin',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_email': cls.user3_email,
                'user_pass': cls.user3_pass,
            }
        )
        print('[...]: Subroutine Execute MasterAccountLogin')
        master_login = cls.core.execute('MasterAccountLogin')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'MasterUnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute MasterUnlinkAccount')
        master_login = cls.core.execute('MasterUnlinkAccount')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'MasterRecoverAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )

    @classmethod
    def tearDownClass(cls):
        set_values = cls.core.set_values(
            'MasterUnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'forced_removal': True,
            }
        )
        unlink_master = cls.core.execute('MasterUnlinkAccount')

    def test_ewcc_set_core_execute_action_master_recover_account_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action MasterRecoverAccount -')
        execute = self.core.execute('MasterRecoverAccount')
        print(
            "[ I ]: core.execute('MasterRecoverAccount') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 4)
        self.assertTrue(isinstance(execute.get('account'), str))
        self.assertTrue(isinstance(execute.get('account_data'), dict))
        self.assertTrue(isinstance(execute.get('session_data'), dict))
        return execute
