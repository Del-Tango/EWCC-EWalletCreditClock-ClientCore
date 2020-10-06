import unittest
# import pysnooper

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionMasterEditAccount(unittest.TestCase):

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

        cls.user3_name = 'EWCC-TestMaster3'
        cls.user3_email = 'master3@ewcc.com'
        cls.user3_pass = 'avsv!@#1234'
        cls.user3_alias = 'TEWCCM3'
        cls.user3_address = 'Jud.Iasi, Iasi, Str.Canta No.40'
        cls.user3_company = 'EWCC-TestCompany'
        cls.master_key_code = 'EWSC-Master-Key-Code'

        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

        print('[ + ]: Prerequisits -')
        # Settups all action and event handlers
        print('[...]: Subroutine Setup Handlers')
        setup_handlers = cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateMaster',
                'MasterAccountLogin', 'MasterAccountLogout',
                'MasterEditAccount', 'MasterUnlinkAccount'
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
            'MasterEditAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': 'EWCC-FTS-Edited',
                'user_email': 'EWCC-FTS-Edited',
                'user_pass': 'EWCC-FTS-Edited!@#123',
                'user_alias': 'EWCC-FTS-Edited',
                'user_phone': 'EWCC-FTS-Edited',
                'company': 'EWCC-FTS-Edited',
                'address': 'EWCC-FTS-Edited',
                'key': 'EWCC-FTS-Edited',

            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'MasterAccountLogout',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('MasterAccountLogout')

        cls.core.set_values(
            'MasterUnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'forced_removal': True,
            }
        )
        cls.core.execute('MasterUnlinkAccount')

    def test_ewcc_set_core_execute_action_master_edit_account_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action MasterEditAccount -')
        execute = self.core.execute('MasterEditAccount')
        print(
            "[ I ]: core.execute('MasterEditAccount') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 4)
        self.assertTrue(isinstance(execute.get('account'), str))
        self.assertTrue(isinstance(execute.get('account_data'), dict))
        self.assertTrue(isinstance(execute.get('edit'), dict))
        return execute
