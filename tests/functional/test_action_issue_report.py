import unittest
import base64

from ewcc_lib import ewallet_client
from ewcc_lib.base import config

config_file = 'conf/ewcc.conf'
config = config.Config()


class TestEwalletClientExecuteActionIssueReport(unittest.TestCase):

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
        setup_handlers = cls.core.setup_handlers(
            handlers=['action'],
            actions=[
                'RequestClientID', 'RequestSessionToken', 'IssueReport',
            ]
        )
        print('[...]: Subroutine Execute RequestClientId')
        cls.client_id = cls.core.execute('RequestClientID')

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'RequestSessionToken',
            **{
                'client_id': cls.client_id.get('client_id')
            }
        )
        print('[...]: Subroutine Execute RequestSessionToken')
        cls.session_token = cls.core.execute('RequestSessionToken')

        log_file_content = '[ ERROR ]: WTF, I did not expect that to happen...'
        content_bytes = log_file_content.encode('ascii')
        base64_bytes = base64.b64encode(content_bytes)
        base64_message = base64_bytes.decode('ascii')
        cls.base64_log = base64_message

        issue_report = {
            'name': 'EWCC-TestSuit',
            'email': cls.user3_email,
            'log': cls.base64_log,
            'details': [
                'Error-Type1', 42, None, {
                    'failed': True,
                    'warning': 'EWCC functional test suit warning message.'
                },
            ],
        }

        print('[...]: Subroutine Set ResourceInstruction')
        set_values = cls.core.set_values(
            'IssueReport',
            **{
                'client_id': cls.client_id.get('client_id'),
                'session_token': cls.session_token.get('session_token'),
                'issue': issue_report,
            }
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_execute_action_issue_report_functional(self):
        print('\n[ * ]: EWCC Subroutine Execute Action IssueReport -')
        execute = self.core.execute('IssueReport')
        print(
            "[ I ]: core.execute('IssueReport') \n"
            + "[ O ]: " + str(execute) + '\n'
        )
        self.assertTrue(isinstance(execute, dict))
        self.assertFalse(execute.get('failed'))
        self.assertEqual(len(execute.keys()), 5)
        self.assertTrue(isinstance(execute.get('contact'), str))
        self.assertTrue(isinstance(execute.get('issue'), str))
        self.assertTrue(isinstance(execute.get('source'), str))
        self.assertTrue(isinstance(execute.get('timestamp'), str))
        return execute
