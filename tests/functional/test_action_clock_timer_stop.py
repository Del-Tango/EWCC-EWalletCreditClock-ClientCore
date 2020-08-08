import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientExecuteActionStopClockTimer(unittest.TestCase):

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
                'AccountLogin', 'UnlinkAccount', 'SupplyCredits',
                'ConvertCreditsToClock', 'StartClockTimer', 'StopClockTimer'
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
            'ConvertCreditsToClock',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'credits': '10',
                'notes': 'Credit2clock conversion notes added by ECC functional tests.'
            }
        )
        print('[...]: Subroutine Execute ConvertCreditsToClock')
        cls.core.execute('ConvertCreditsToClock')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'StartClockTimer',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        print('[...]: Subroutine Execute StartClockTimer')
        cls.core.execute('StartClockTimer')
        print('[...]: Subroutine Set ResourceInstruction')
        cls.core.set_values(
            'StopClockTimer',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.core.set_values(
            'UnlinkAccount',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
            }
        )
        cls.core.execute('UnlinkAccount')

    def test_ewcc_set_core_execute_action_stop_clock_timer_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action StopClockTimer -')
        execute = self.core.execute('StopClockTimer')
        print(
            "[ I ]: core.execute('StopClockTimer') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 9)
        self.assertTrue(isinstance(execute.get('clock'), int))
        self.assertTrue(isinstance(execute.get('start_timestamp'), str))
        self.assertTrue(isinstance(execute.get('stop_timestamp'), str))
        self.assertTrue(isinstance(execute.get('minutes_spent'), float))
        self.assertTrue(isinstance(execute.get('pending_count'), int))
        self.assertTrue(isinstance(execute.get('pending_time'), float))
        self.assertTrue(isinstance(execute.get('time_record'), int))
        self.assertTrue(isinstance(execute.get('record_data'), dict))
        return execute
