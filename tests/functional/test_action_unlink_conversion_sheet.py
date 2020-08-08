import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionUnlinkConversionSheet(unittest.TestCase):

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
                'AccountLogin', 'UnlinkAccount', 'UnlinkConversionSheet',
                'ViewCreditClock', 'CreateConversionSheet',
                'SwitchConversionSheet'
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
            'ViewCreditClock',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute AccountLogin')
        cls.response = cls.core.execute('ViewCreditClock')
        cls.conversion_sheet = cls.response['clock_data']['conversion_sheet']
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'UnlinkConversionSheet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'list_id': cls.conversion_sheet,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'CreateConversionSheet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        response = cls.core.execute('CreateConversionSheet')
        cls.core.set_values(
            'SwitchConversionSheet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'sheet_id': response['conversion_sheet'],
            }
        )
        cls.core.execute('SwitchConversionSheet')
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_unlink_conversion_sheet_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action UnlinkConversionSheet -')
        execute = self.core.execute('UnlinkConversionSheet')
        print(
            "[ I ]: core.execute('UnlinkConversionSheet') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 2)
        self.assertTrue(isinstance(execute.get('conversion_sheet'), int))
        return execute
