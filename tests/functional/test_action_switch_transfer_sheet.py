import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionSwitchTransferSheet(unittest.TestCase):

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
        cls.core = EWalletClientCore(config_file=config_file)

        print('[ + ]: Prerequisits -')
        # Settups all action and event handlers
        print('[...]: Subroutine Setup Handlers')
        cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'CreateNewAccount',
                'AccountLogin', 'UnlinkAccount', 'SwitchTransferSheet',
                'ViewCreditEWallet'
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
                'user_name': cls.user1_name,
                'user_email': cls.user1_email,
                'user_pass': cls.user1_pass,
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
                'user_email': cls.user1_email,
                'user_pass': cls.user1_pass,
            }
        )
        print('[...]: Subroutine Execute AccountLogin')
        cls.core.execute('AccountLogin')

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'ViewCreditEWallet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute ViewAccount')
        cls.response = cls.core.execute('ViewCreditEWallet')

        ewallet_data = cls.response.get('ewallet_data')
        cls.current_transfer_sheet = int() if not ewallet_data else \
            cls.response['ewallet_data']['transfer_sheet']
        cls.new_transfer_sheet = int() if not ewallet_data else int(
            list(
                cls.response['ewallet_data']['transfer_sheet_archive'].keys()
            )[0]
        )

        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'SwitchTransferSheet',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'sheet_id': cls.new_transfer_sheet,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'SwitchTransferSheet',
            **{
                'sheet_id': cls.current_transfer_sheet,
            }
        )
        cls.core.execute('SwitchTransferSheet')
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_switch_transfer_sheet_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action SwitchTransferSheet -')
        execute = self.core.execute('SwitchTransferSheet')
        print(
            "[ I ]: core.execute('SwitchTransferSheet') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 3)
        self.assertTrue(isinstance(execute.get('transfer_sheet'), int))
        self.assertTrue(isinstance(execute.get('sheet_data'), dict))
        return execute
