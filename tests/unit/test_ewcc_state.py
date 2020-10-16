import unittest

from ewcc_lib import ewallet_client


class TestEwalletClientCoreState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_state_unit(self):
        print('[ * ]: EWCC Subroutine State -')
        core_state = self.core.state()
        print(
            "[ I ]: core.state() \n"
            + "[ O ]: " + str(core_state) + '\n'
        )
        self.assertTrue(isinstance(core_state, dict))
        self.assertFalse(core_state.get('failed'))
        self.assertTrue(isinstance(core_state.get('state'), dict))
        self.assertTrue(isinstance(core_state['state'].get('actions'), dict))
        self.assertTrue(isinstance(core_state['state'].get('events'), dict))
        self.assertTrue(isinstance(core_state['state'].get('status'), bool))
        self.assertTrue(isinstance(core_state['state'].get('instruction_set'), dict))
        self.assertTrue(isinstance(core_state['state'].get('instruction_set_response'), dict))
        self.assertTrue(True if 'response' in core_state['state'] else False)
        self.assertTrue(True if 'timestamp' in core_state['state'] else False)
        self.assertTrue(isinstance(core_state['state'].get('config_file'), str))
        self.assertTrue(isinstance(core_state['state'].get('config'), dict))
        self.assertTrue(isinstance(core_state['state']['config'].get('log_config'), dict))
        self.assertTrue(isinstance(core_state['state']['config'].get('cloud_config'), dict))
        self.assertTrue(isinstance(core_state['state'].get('previous_action'), str))
        self.assertTrue(isinstance(core_state['state'].get('previous_event'), str))
        return core_state
