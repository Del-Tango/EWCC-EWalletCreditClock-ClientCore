import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCoreSetupHandlers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)
        cls.available_events = []
        cls.available_actions = [
            'RequestClientID',
            'RequestSessionToken',
            'PauseClockTimer',
            'ResumeClockTimer',
            'StartClockTimer',
            'StopClockTimer',
            'AccountLogin',
            'AccountLogout',
            'AddContactRecord',
            'ConvertClockToCredits',
            'ConvertCreditsToClock',
            'CreateNewAccount',
            'CreateContactList',
            'CreateConversionSheet',
            'CreateCreditClock',
            'CreateCreditEWallet',
            'CreateInvoiceSheet',
            'CreateTimeSheet',
            'CreateTransferSheet',
            'EditAccount',
            'PayCredits',
            'SupplyCredits',
            'SwitchActiveSessionUser',
            'SwitchContactList',
            'SwitchConversionSheet',
            'SwitchCreditClock',
            'SwitchCreditEWallet',
            'SwitchInvoiceSheet',
            'SwitchTimeSheet',
            'SwitchTransferSheet',
            'TransferCredits',
            'UnlinkAccount',
            'UnlinkContactList',
            'UnlinkContactRecord',
            'UnlinkConversionRecord',
            'UnlinkConversionSheet',
            'UnlinkCreditClock',
            'UnlinkCreditEWallet',
            'UnlinkInvoiceRecord',
            'UnlinkInvoiceSheet',
            'UnlinkTimeRecord',
            'UnlinkTimeSheet',
            'UnlinkTransferRecord',
            'UnlinkTransferSheet',
            'ViewAccount',
            'ViewContactList',
            'ViewContactRecord',
            'ViewConversionRecord',
            'ViewConversionSheet',
            'ViewCreditClock',
            'ViewCreditEWallet',
            'ViewInvoiceRecord',
            'ViewInvoiceSheet',
            'ViewLoginRecords',
            'ViewLogoutRecords',
            'ViewTimeRecord',
            'ViewTimeSheet',
            'ViewTransferRecord',
            'ViewTransferSheet',
        ]

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_setup_all_handlers_unit(self):
        print('[ * ]: EWCC Subroutine SetupHandlers -')
        setup_handlers = self.core.setup_handlers()
        print(
            "[ I ]: core.setup_handlers() \n"
            + "[ O ]: " + str(setup_handlers) + '\n'
        )
        return setup_handlers

    def test_ewcc_setup_specific_action_handlers_unit(self):
        print('[ * ]: EWCC Subroutine SetupSpecificActionHandlers -')
        setup_handlers = self.core.setup_handlers(**{
            'handlers': ['action'],
            'actions': self.available_actions
        })
        print(
            "[ I ]: core.setup_handlers(handlers=['action'], actions=<action-label-set>) \n"
            + "[ O ]: " + str(setup_handlers) + '\n'
        )
        self.assertTrue(isinstance(setup_handlers, dict))
        self.assertTrue(isinstance(setup_handlers.get('actions'), dict))
        self.assertEqual(len(setup_handlers['actions']), len(self.available_actions) + 1)
        self.assertFalse(setup_handlers.get('events'))
        return setup_handlers

    def test_ewcc_setup_specific_event_handlers_unit(self):
        print('[ * ]: EWCC Subroutine SetupSpecificEventHandlers -')
        setup_handlers = self.core.setup_handlers(**{
            'handlers': ['event'],
            'events': self.available_events
        })
        print(
            "[ I ]: core.setup_handlers(handlers=['event'], events=<event-label-set>) \n"
            + "[ O ]: " + str(setup_handlers) + '\n')
        self.assertTrue(isinstance(setup_handlers, dict))
        self.assertTrue(isinstance(setup_handlers.get('events'), dict))
        self.assertTrue(setup_handlers['events'].get('failed'))
#       self.assertEqual(len(setup_handlers['events']), len(self.available_events) + 1)
        self.assertFalse(setup_handlers.get('actions'))
        return setup_handlers

    def test_ewcc_setup_specific_handlers_unit(self):
        print('[ * ]: EWCC Subroutine SetupSpecificHandlers -')
        setup_handlers = self.core.setup_handlers(**{
            'handlers': ['action', 'event'],
            'actions': self.available_actions,
            'events': self.available_events
        })
        print(
            "[ I ]: core.setup_handlers(handlers=['action', 'event'], "
            "actions=<action-label-set>, events=<event-label-set>) \n"
            + "[ O ]: " + str(setup_handlers) + '\n')
        self.assertTrue(isinstance(setup_handlers, dict))
        self.assertTrue(isinstance(setup_handlers.get('actions'), dict))
        self.assertTrue(isinstance(setup_handlers.get('events'), dict))
        self.assertEqual(len(setup_handlers['actions']), len(self.available_actions) + 1)
        self.assertTrue(setup_handlers['events'].get('failed'))
#       self.assertEqual(len(setup_handlers['events']), len(self.available_events) + 1)
        return setup_handlers
