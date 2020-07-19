import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCoreSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_values_implicitly_unit(self):
        print('[ * ]: EWallet Client Core Set Core Values Implicitly')
        set_core = self.core.set_values('', {'config_file': 'test/edited.conf'})
        print(
            "[ I ]: core.set_values('', {'config_file': 'test/edited.conf'}) \n"
            + "[ O ]: " + str(set_core) + '\n'
        )
        self.assertTrue(isinstance(set_core, dict))
        self.assertFalse(set_core.get('failed'))
        self.assertEqual(len(set_core.keys()), 3)
        self.assertTrue(isinstance(set_core.get('updated'), list))
        self.assertTrue(isinstance(set_core.get('state'), dict))
        return set_core

    def test_ewcc_set_core_values_explicitly_unit(self):
        print('[ * ]: EWallet Client Core Set Core Values Explicity')
        set_core = self.core.set_values('Core', {'config_file': 'test2/edited.conf'})
        print(
            "[ I ]: core.set_values('Core', {'config_file': 'test2/edited.conf'}) \n"
            + "[ O ]: " + str(set_core) + '\n'
        )
        self.assertTrue(isinstance(set_core, dict))
        self.assertFalse(set_core.get('failed'))
        self.assertEqual(len(set_core.keys()), 3)
        self.assertTrue(isinstance(set_core.get('updated'), list))
        self.assertTrue(isinstance(set_core.get('state'), dict))
        return set_core

    def test_ewcc_set_core_config_values_unit(self):
        print('[ * ]: EWallet Client Core Set Core Config Values')
        set_config = self.core.set_values('Config', {'config_file': 'test3/edited.conf'})
        print(
            "[ I ]: core.set_values('Config', {'config_file': 'test3/edited.conf'}) \n"
            + "[ O ]: " + str(set_config) + '\n'
        )
        self.assertTrue(isinstance(set_config, dict))
        self.assertFalse(set_config.get('failed'))
        self.assertEqual(len(set_config.keys()), 3)
        self.assertTrue(isinstance(set_config.get('updated'), list))
        self.assertTrue(isinstance(set_config.get('config'), dict))
        return set_config
