import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionUnlinkCreditEWallet(unittest.TestCase):

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
                'AccountLogin', 'UnlinkAccount', 'UnlinkCreditEWallet',
                'ViewAccount', 'CreateCreditEWallet', 'SwitchCreditEWallet'
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
            'ViewAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute ViewAccount')
        cls.response = cls.core.execute('ViewAccount')
        cls.ewallet = cls.response['account_data']['ewallet']
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'UnlinkCreditEWallet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'ewallet_id': cls.ewallet,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'CreateCreditEWallet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        response = cls.core.execute('CreateCreditEWallet')
        cls.core.set_values(
            'SwitchCreditEWallet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'ewallet_id': response['ewallet'],
            }
        )
        cls.core.execute('SwitchCreditEWallet')
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_unlink_credit_ewallet_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action UnlinkCreditEWallet -')
        execute = self.core.execute('UnlinkCreditEWallet')
        print(
            "[ I ]: core.execute('UnlinkCreditEWallet') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 2)
        self.assertTrue(isinstance(execute.get('credit_ewallet'), int))
        return execute
