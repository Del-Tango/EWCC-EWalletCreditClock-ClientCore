import unittest
import pysnooper

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientPrevious(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)
        # Settups all action and event handlers
        cls.core.setup_handlers()

    @classmethod
    def tearDownClass(cls):
        pass

#   @pysnooper.snoop()
    def test_ewcc_previous_unit(self):
        print('[ * ]: EWallet Client Core Previous')
        self.core.execute('RequestClientID')
        previous = self.core.previous()
        print(
            "[ I ]: core.previous() \n"
            + "[ O ]: " + str(previous) + '\n'
        )
        self.assertTrue(isinstance(previous, dict))
        self.assertFalse(previous.get('failed'))
        self.assertEqual(len(previous.keys()), 3)
        self.assertTrue(isinstance(previous.get('execution'), str))
        self.assertTrue(isinstance(previous.get('previous'), str))
        self.assertEqual(previous.get('execution'), 'action')
        self.assertEqual(previous.get('previous'), 'RequestClientID')
        return previous

    def test_ewcc_previous_action_unit(self):
        print('[ * ]: EWallet Client Core Previous Action')
        self.core.execute('RequestClientID')
        previous = self.core.previous('action')
        print(
            "[ I ]: core.previous('action') \n"
            + "[ O ]: " + str(previous) + '\n'
        )
        self.assertTrue(isinstance(previous, dict))
        self.assertFalse(previous.get('failed'))
        self.assertEqual(len(previous.keys()), 2)
        self.assertTrue(isinstance(previous.get('action'), str))
        self.assertEqual(previous.get('action'), 'RequestClientID')
        return previous

    def test_ewcc_previous_event_unit(self):
        print('[ * ]: EWallet Client Core Previous Event')
        previous = self.core.previous('event')
        print(
            "[ I ]: core.previous('event') \n"
            + "[ O ]: " + str(previous) + '\n'
        )
        self.assertTrue(isinstance(previous, dict))
        self.assertFalse(previous.get('failed'))
        self.assertEqual(len(previous.keys()), 2)
        self.assertTrue(isinstance(previous.get('event'), str))
        return previous

    def test_ewcc_previous_specific_action_unit(self):
        print('[ * ]: EWallet Client Core Previous Specific Action')
        self.core.execute('RequestClientID')
        previous = self.core.previous('RequestClientID')
        print(
            "[ I ]: core.previous('RequestClientID') \n"
            + "[ O ]: " + str(previous) + '\n'
        )
        self.assertTrue(isinstance(previous, dict))
        self.assertFalse(previous.get('failed'))
        return previous
