import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionMasterViewAccount(unittest.TestCase):

    @classmethod
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
        cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateMaster',
                'MasterAccountLogin', 'MasterAccountLogout',
                'MasterViewAccount', #'MasterUnlinkAccount'
            ]
        )
        print('[...]: Subroutine Execute RequestClientId')
        cls.client_id = cls.core.execute('RequestClientID')

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'RequestSessionToken',
            **{
                'client_id': cls.client_id.get('client_id')
            }
        )
        print('[...]: Subroutine Execute RequestSessionToken')
        cls.session_token = cls.core.execute('RequestSessionToken')

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
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
                'key': cls.master_key_code,
            }
        )
        print('[...]: Subroutine Execute CreateMaster')
        cls.core.execute('CreateMaster')

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'MasterAccountLogin',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_email': cls.user3_email,
                'user_pass': cls.user3_pass,
            }
        )
        print('[...]: Subroutine Execute MasterAccountLogin')
        cls.core.execute('MasterAccountLogin')

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'MasterViewAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )

    @classmethod
    def tearDownClass(cls):
        pass
        cls.core.set_values(
            'MasterAccountLogout',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('MasterAccountLogout')

#       cls.core.set_values(
#           'MasterUnlinkAccount',
#           **{
#               'client_id': cls.client_id.get('client_id'),
#               'session_token': cls.session_token.get('session_token'),
#               'forced_removal': True,
#           }
#       )
#       cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_master_view_account_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action MasterViewAccount -')
        execute = self.core.execute('MasterViewAccount')
        print(
            "[ I ]: core.execute('MasterViewAccount') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 3)
        self.assertTrue(isinstance(execute.get('account'), str))
        self.assertTrue(isinstance(execute.get('account_data'), dict))
        return execute
