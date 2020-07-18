import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCoreState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_state_unit(self):
        print('[ * ]: EWallet Client Core Config')
        core_state = self.core.state()
        print(str(core_state) + '\n')
        self.assertTrue(isinstance(core_state, dict))
        self.assertTrue(isinstance(core_state.get('actions'), dict))
        self.assertTrue(isinstance(core_state.get('events'), dict))
        self.assertTrue(isinstance(core_state.get('status'), bool))
        self.assertTrue(isinstance(core_state.get('instruction_set'), dict))
        self.assertTrue(isinstance(core_state.get('instruction_set_response'), dict))
        self.assertTrue(True if 'response' in core_state else False)
        self.assertTrue(True if 'timestamp' in core_state else False)
        self.assertTrue(isinstance(core_state.get('config_file'), str))
        self.assertTrue(isinstance(core_state.get('config'), dict))
        self.assertTrue(isinstance(core_state['config'].get('log_config'), dict))
        self.assertTrue(isinstance(core_state['config'].get('cloud_config'), dict))
        self.assertTrue(isinstance(core_state.get('previous_action'), str))
        self.assertTrue(isinstance(core_state.get('previous_event'), str))
        return core_state
