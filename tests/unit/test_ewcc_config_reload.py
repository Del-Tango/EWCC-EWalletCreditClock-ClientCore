import unittest

from ewcc_lib import ewallet_client


class TestEwalletClientConfigReload(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_config_reload_unit(self):
        print('[ * ]: EWCC Subroutine ConfigReload -')
        config_reload = self.core.config_reload(self.core.config_file)
        print(
            "[ I ]: core.config_reload(<config-file>) \n"
            + "[ O ]: " + str(config_reload) + '\n'
        )
        self.assertTrue(isinstance(config_reload, dict))
        self.assertFalse(config_reload.get('failed'))
        self.assertEqual(len(config_reload.keys()), 2)
        self.assertTrue(config_reload.get('config'))
        self.assertTrue(isinstance(config_reload['config'], dict))
        self.assertFalse(config_reload['config'].get('failed'))
        self.assertTrue(config_reload['config']['config_timestamp'])
        self.assertTrue(isinstance(config_reload['config']['config_file'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config'], dict))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-name'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-level'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-dir'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-file'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-path'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-record-format'], str))
        self.assertTrue(isinstance(config_reload['config']['log_config']['log-date-format'], str))
        self.assertTrue(isinstance(config_reload['config']['cloud_config'], dict))
        self.assertTrue(isinstance(config_reload['config']['cloud_config']['ewsc-address'], str))
        self.assertTrue(isinstance(config_reload['config']['cloud_config']['ewsc-port'], int))
        self.assertTrue(isinstance(config_reload['config']['cloud_config']['ewsc-url'], str))
        return config_reload
