import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionUnlinkContactRecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)
        print('[ + ]: Prerequisits -')
        # Settups all action and event handlers
        print('[...]: Subroutine Setup Handlers')
        cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateNewAccount',
                'AccountLogin', 'UnlinkAccount', 'UnlinkContactRecord',
                'ViewContactList', 'AddContactRecord'
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
            'CreateNewAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': 'EWCC-TestUserName',
                'user_email': 'test@ewcc.com',
                'user_pass': '1234abcs!@#$'
            }
        )
        print('[...]: Subroutine Execute CreateNewAccount')
        cls.core.execute('CreateNewAccount')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'AccountLogin',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': 'EWCC-TestUserName',
                'user_pass': '1234abcs!@#$',
            }
        )
        print('[...]: Subroutine Execute AccountLogin')
        cls.core.execute('AccountLogin')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'AddContactRecord',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': 'TestContactRecord',
                'user_email': 'test@contact.com',
                'user_reference': 'TContact',
                'user_phone': '555 555 555',
                'notes': 'Notes added by EWCC functional test suit.',
            }
        )
        print('[...]: Subroutine Execute AddContactRecord')
        cls.response = cls.core.execute('AddContactRecord')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'ViewContactList',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute ViewContactList')
        cls.response = cls.core.execute('ViewContactList')
        records = cls.response['list_data']['records']
        cls.record = None if not records else int(list(records.keys())[0])
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'UnlinkContactRecord',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'record_id': cls.record,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'AddContactRecord',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'user_name': 'TestContactRecord',
                'user_email': 'test@contact.com',
                'user_reference': 'TContact',
                'user_phone': '555 555 555',
                'notes': 'Notes added by EWCC functional test suit.',
            }
        )
        cls.response = cls.core.execute('AddContactRecord')
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_unlink_contact_record_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action UnlinkContactRecord -')
        execute = self.core.execute('UnlinkContactRecord')
        print(
            "[ I ]: core.execute('UnlinkContactRecord') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 3)
        self.assertTrue(isinstance(execute.get('contact_list'), int))
        self.assertTrue(isinstance(execute.get('contact_record'), int))
        return execute
