import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientCoreNewHandlers(unittest.TestCase):

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

    def test_ewcc_new_handlers_unit(self):
        print('[ * ]: EWCC Subroutine NewHandlers -')
        new_handlers = self.core.new(new='handlers')
        print(
            "[ I ]: core.new(new='handlers') \n"
            + "[ O ]: " + str(new_handlers) + '\n'
        )
        return new_handlers

    def test_ewcc_new_specific_action_handlers_unit(self):
        print('[ * ]: EWCC Subroutine NewSpecificActionHandlers -')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['action'],
            'actions': self.available_actions
        })
        print(
            "[ I ]: core.new(new='handlers', handlers=['action'], "
            "actions=<action-label-set>) \n"
            + "[ O ]: " + str(new_handlers) + '\n'
        )
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('actions'), dict))
        self.assertEqual(len(new_handlers['actions']), len(self.available_actions) + 1)
        return new_handlers

    def test_ewcc_new_specific_event_handlers_unit(self):
        print('[ * ]: EWCC Subroutine NewSpecificEventHandlers -')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['event'],
            'events': self.available_events
        })
        print(
            "[ I ]: core.new(new='handlers', handlers=['event'], events=<event-label-set>) \n"
            + "[ O ]: " + str(new_handlers) + '\n'
        )
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('events'), dict))
        self.assertTrue(new_handlers['events'].get('failed'))
#       self.assertEqual(len(new_handlers['events']), len(self.available_events) + 1)
        return new_handlers

    def test_ewcc_new_specific_handlers_unit(self):
        print('[ * ]: EWCC Subroutine NewSpecificHandlers -')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['action', 'event'],
            'actions': self.available_actions,
            'events': self.available_events
        })
        print(
            "[ I ]: core.new(new='handlers', handlers=['action', 'event'], "
            "actions=<action-label-set>, events=<event-label-set>) \n"
            + "[ O ]: " + str(new_handlers) + '\n'
        )
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('actions'), dict))
        self.assertTrue(isinstance(new_handlers.get('events'), dict))
        self.assertEqual(len(new_handlers['actions']), len(self.available_actions) + 1)
#       self.assertEqual(len(new_handlers['events']), len(self.available_events) + 1)
        self.assertTrue(new_handlers['events'].get('failed'))
        return new_handlers
