import unittest

from ewcc_lib import ewallet_client

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionAddContactRecord(unittest.TestCase):

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

        # Instantiate EWCC with specified config file
        cls.core = ewallet_client.EWalletClientCore()

        print('[ + ]: Prerequisits -')

        print('[...]: Subroutine Setup Handlers')
        set_values = cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateAccount',
                'AccountLogin', 'UnlinkAccount', 'AddContactRecord',
                'CreateMaster', 'AcquireMaster', 'MasterAccountLogin',
                'MasterUnlinkAccount',
            ]
        )
        print('[...]: Subroutine Execute RequestClientId')
        request_ctoken = cls.client_id = cls.core.execute('RequestClientID')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'RequestSessionToken',
            **{
                'client_id': cls.client_id.get('client_id')
            }
        )
        print('[...]: Subroutine Execute RequestSessionToken')
        request_stoken = cls.session_token = cls.core.execute('RequestSessionToken')

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
            'AcquireMaster',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'master': cls.user3_email,
                'key': cls.master_key_code,
            }
        )
        print('[...]: Subroutine Execute AcquireMaster')
        acquire_master = cls.core.execute('AcquireMaster')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'CreateAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': cls.user1_name,
                'user_email': cls.user1_email,
                'user_pass': cls.user1_pass
            }
        )
        print('[...]: Subroutine Execute CreateAccount')
        create_account = cls.core.execute('CreateAccount')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'AccountLogin',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_email': cls.user1_email,
                'user_pass': cls.user1_pass,
            }
        )
        print('[...]: Subroutine Execute AccountLogin')
        account_login = cls.core.execute('AccountLogin')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'AddContactRecord',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_email': 'test@contact.mail',
                'user_name': 'TestContact',
                'user_phone': '555 555 555',
                'user_reference': 'TContact',
                'notes': 'Contact record notes added by '
                         'EWCC functional test suit.',
            }
        )

    @classmethod
    def tearDownClass(cls):
        set_values = cls.core.set_values(
            'MasterAccountLogin',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_email': cls.user3_email,
                'user_pass': cls.user3_pass,
            }
        )
        master_login = cls.core.execute('MasterAccountLogin')

        set_values = cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'forced_removal': True,
            }
        )
        unlink_account = cls.core.execute('UnlinkAccount')

        set_values = cls.core.set_values(
            'MasterUnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'forced_removal': True,
            }
        )
        unlink_master = cls.core.execute('MasterUnlinkAccount')

    def test_ewcc_set_core_execute_action_add_contact_record_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action AddContactRecord -')
        execute = self.core.execute('AddContactRecord')
        print(
            "[ I ]: core.execute('AddContactRecord') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 3)
        self.assertTrue(isinstance(execute.get('contact_list'), int))
        self.assertTrue(isinstance(execute.get('contact_record'), int))
        return execute
