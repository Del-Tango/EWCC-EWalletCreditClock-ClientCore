import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionUnlinkInvoiceRecord(unittest.TestCase):

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
                'AccountLogin', 'UnlinkAccount', 'UnlinkInvoiceRecord',
                'ViewInvoiceSheet', 'SupplyCredits', 'PayCredits'
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
            'SupplyCredits',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'credits': 10,
                'currency': 'RON',
                'cost': 4.7,
                'notes': 'Notes added by EWCC functional test suit.'
            }
        )
        print('[...]: Subroutine Execute SupplyCredits')
        cls.core.execute('SupplyCredits')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'PayCredits',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'pay': 'ewsc.systemcore@alvearesolutions.ro',
                'credits': '5',
            }
        )
        print('[...]: Subroutine Execute PayCredits')
        cls.core.execute('PayCredits')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'ViewInvoiceSheet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute ViewInvoiceSheet')
        cls.response = cls.core.execute('ViewInvoiceSheet')
        records = cls.response['sheet_data']['records']
        cls.record = None if not records else int(list(records.keys())[0])
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'UnlinkInvoiceRecord',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'record_id': cls.record,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'PayCredits',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'pay': 'ewsc.systemcore@alvearesolutions.ro',
                'credits': '5',
            }
        )
        cls.core.execute('PayCredits')
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_unlink_invoice_record_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action UnlinkInvoiceRecord -')
        execute = self.core.execute('UnlinkInvoiceRecord')
        print(
            "[ I ]: core.execute('UnlinkInvoiceRecord') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 3)
        self.assertTrue(isinstance(execute.get('invoice_sheet'), int))
        self.assertTrue(isinstance(execute.get('invoice_record'), int))
        return execute
