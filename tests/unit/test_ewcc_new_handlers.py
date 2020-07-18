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
        print('[ * ]: EWallet Client Core New Handlers')
        new_handlers = self.core.new(new='handlers')
        print(str(new_handlers) + '\n')
        return new_handlers

    def test_ewcc_new_specific_action_handlers_unit(self):
        print('[ * ]: EWallet Client Core New Specific Action Handlers')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['action'],
            'actions': self.available_actions
        })
        print(str(new_handlers) + '\n')
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('actions'), dict))
        self.assertTrue(isinstance(new_handlers.get('events'), dict))
        self.assertEqual(len(new_handlers['actions']), len(self.available_actions))
        self.assertEqual(len(new_handlers['events']), len(self.available_events))
        return new_handlers

    def test_ewcc_new_specific_event_handlers_unit(self):
        print('[ * ]: EWallet Client Core New Specific Event Handlers')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['event'],
            'events': self.available_events
        })
        print(str(new_handlers) + '\n')
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('actions'), dict))
        self.assertTrue(isinstance(new_handlers.get('events'), dict))
        self.assertEqual(len(new_handlers['actions']), len(self.available_actions))
        self.assertEqual(len(new_handlers['events']), len(self.available_events))
        return new_handlers

    def test_ewcc_new_specific_handlers_unit(self):
        print('[ * ]: EWallet Client Core New Specific Handlers')
        new_handlers = self.core.new(**{
            'new': 'handlers',
            'handlers': ['action', 'event'],
            'actions': self.available_actions,
            'events': self.available_events
        })
        print(str(new_handlers) + '\n')
        self.assertTrue(isinstance(new_handlers, dict))
        self.assertTrue(isinstance(new_handlers.get('actions'), dict))
        self.assertTrue(isinstance(new_handlers.get('events'), dict))
        self.assertEqual(len(new_handlers['actions']), len(self.available_actions))
        self.assertEqual(len(new_handlers['events']), len(self.available_events))
        return new_handlers
