import unittest

from ewcc_lib import ewallet_client


class TestEwalletClientCoreSet(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()
        cls.core.setup_handlers()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_set_core_values_implicitly_unit(self):
        print('[ * ]: EWCC Subroutine SetCoreValues Implicitly -')
        set_core = self.core.set_values('', **{'config_file': 'test/edited.conf'})
        print(
            "[ I ]: core.set_values('', **{'config_file': 'test/edited.conf'}) \n"
            + "[ O ]: " + str(set_core) + '\n'
        )
        self.assertTrue(isinstance(set_core, dict))
        self.assertFalse(set_core.get('failed'))
        self.assertEqual(len(set_core.keys()), 3)
        self.assertTrue(isinstance(set_core.get('updated'), list))
        self.assertTrue(isinstance(set_core.get('state'), dict))
        return set_core

    def test_ewcc_set_core_values_explicitly_unit(self):
        print('[ * ]: EWCC Subroutine SetCoreValues Explicity -')
        set_core = self.core.set_values('Core', **{'config_file': 'test2/edited.conf'})
        print(
            "[ I ]: core.set_values('Core', **{'config_file': 'test2/edited.conf'}) \n"
            + "[ O ]: " + str(set_core) + '\n'
        )
        self.assertTrue(isinstance(set_core, dict))
        self.assertFalse(set_core.get('failed'))
        self.assertEqual(len(set_core.keys()), 3)
        self.assertTrue(isinstance(set_core.get('updated'), list))
        self.assertTrue(isinstance(set_core.get('state'), dict))
        return set_core

    def test_ewcc_set_core_config_values_unit(self):
        print('[ * ]: EWCC Subroutine SetConfigValues -')
        set_config = self.core.set_values('Config', **{'config_file': 'test3/edited.conf'})
        print(
            "[ I ]: core.set_values('Config', **{'config_file': 'test3/edited.conf'}) \n"
            + "[ O ]: " + str(set_config) + '\n'
        )
        self.assertTrue(isinstance(set_config, dict))
        self.assertFalse(set_config.get('failed'))
        self.assertEqual(len(set_config.keys()), 3)
        self.assertTrue(isinstance(set_config.get('updated'), list))
        self.assertTrue(isinstance(set_config.get('config'), dict))
        return set_config

    def test_ewcc_set_resource_instruction_unit(self):
        print('[ * ]: EWCC Subroutine SetResourceInstruction -')
        request = self.core.execute('RequestClientID')
        set_instruction = self.core.set_values(
            'RequestSessionToken', **{'client_id': request['client_id']}
        )
        print(
            "[ I ]: core.set_values('RequestSessionToken', **{'client_id': request['client_id']}) \n"
            + "[ O ]: " + str(set_instruction) + '\n'
        )
        self.assertTrue(isinstance(set_instruction, dict))
        self.assertFalse(set_instruction.get('failed'))
        self.assertTrue(isinstance(set_instruction.get('updated'), list))
        self.assertTrue(isinstance(set_instruction['updated'][0], str))
        self.assertEqual(set_instruction['updated'][0], 'client_id')
        self.assertTrue(isinstance(set_instruction.get('instruction_set'), dict))
        self.assertTrue(set_instruction['instruction_set'].get('client_id'))
        self.assertTrue(isinstance(set_instruction['instruction_set']['client_id'], str))
        return set_instruction








