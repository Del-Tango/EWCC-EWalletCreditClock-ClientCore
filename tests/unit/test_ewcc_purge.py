import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCorePurge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)
        cls.core.setup_handlers(
            handlers=['action'], actions=['RequestClientID', 'RequestSessionToken']
        )
#       cls.core.setup_handlers()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_purge_all_values_unit(self):
        print('[ * ]: EWCC Subroutine Purge -')
        purge_core = self.core.purge()
        print(
            "[ I ]: core.purge() \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['core'], dict))
        self.assertTrue(isinstance(purge_core['resource'], dict))
        self.assertFalse(purge_core['core'].get('failed'))
        self.assertTrue(isinstance(purge_core['resource'].get('failed'), bool))
        return purge_core

    def test_ewcc_purge_core_values_implicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeCore Implicitly -')
        purge_core = self.core.purge('')
        print(
            "[ I ]: core.purge('') \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue(isinstance(purge_core['state'], dict))
        return purge_core

    def test_ewcc_purge_specific_core_values_implicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeSpecificCoreValues Implicitly -')
        purge_core = self.core.purge('', purge=['config_file'])
        print(
            "[ I ]: core.purge('', purge=['config_file']) \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue('config_file' in purge_core['updated'])
        self.assertTrue(isinstance(purge_core['state'], dict))
        return purge_core

    def test_ewcc_purge_core_values_explicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeCore Explicitly -')
        purge_core = self.core.purge('Core')
        print(
            "[ I ]: core.purge('Core') \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue(isinstance(purge_core['state'], dict))
        return purge_core

    def test_ewcc_purge_specific_core_values_explicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeSpecificCoreValues Explicitly -')
        purge_core = self.core.purge('Core', purge=['config_file'])
        print(
            "[ I ]: core.purge('Core', purge=['config_file']) \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue('config_file' in purge_core['updated'])
        self.assertTrue(isinstance(purge_core['state'], dict))
        return purge_core

    def test_ewcc_purge_config_values_explicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeConfig -')
        purge_core = self.core.purge('Config')
        print(
            "[ I ]: core.purge('Config') \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue(isinstance(purge_core['config'], dict))
        return purge_core

    def test_ewcc_purge_specific_config_values_explicitly_unit(self):
        print('[ * ]: EWCC Subroutine PurgeSpecificConfigValues -')
        purge_core = self.core.purge('Config', purge=['config_file'])
        print(
            "[ I ]: core.purge('Config', purge=['config_file']) \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(isinstance(purge_core['updated'], list))
        self.assertTrue('config_file' in purge_core['updated'])
        self.assertTrue(isinstance(purge_core['config'], dict))
        return purge_core

    def test_ewcc_purge_resource_values_unit(self):
        print('[ * ]: EWCC Subroutine PurgeResourceHandlers -')
        self.core.setup_handlers()
        purge_core = self.core.purge('Resource')
        print(
            "[ I ]: core.purge('Resource') \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        return purge_core

    def test_ewcc_purge_action_resource_handlers_value_set_unit(self):
        print('[ * ]: EWCC Subroutine PurgeActionResourceHandlers -')
        self.core.setup_handlers()
        purge_core = self.core.purge('Resource', actions=True)
        print(
            "[ I ]: core.purge('Resource', actions=True) \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        return purge_core

    def test_ewcc_purge_action_resource_handlers_specified_value_set_unit(self):
        print('[ * ]: EWCC Subroutine PurgeSpecificActionResourceHandlerValues')
        self.core.setup_handlers(handlers=['action'], actions=['RequestClientID'])
        purge_core = self.core.purge(
            'Resource', actions=True, purge=['instruction_set']
        )
        print(
            "[ I ]: core.purge('Resource', actions=True, purge=['instruction_set']) \n"
            + "[ O ]: " + str(purge_core) + '\n'
        )
        self.assertTrue(isinstance(purge_core, dict))
        self.assertFalse(purge_core.get('failed'))
        self.assertTrue(purge_core.get('RequestClientID'))
        self.assertTrue(isinstance(purge_core['RequestClientID'], dict))
        return purge_core
