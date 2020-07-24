import unittest

from ewallet_client import EWalletClientCore

config_file = 'conf/ewcc.conf'


class TestEwalletClientServerOnline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate CC with specified config file
        cls.core = EWalletClientCore(config_file=config_file)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_server_online_unit(self):
        print('[ * ]: EWCC Subroutine ServerOnline -')
        self.core.config_reload(config_file)
        response = self.core.server_online()
        print(
            "[ I ]: core.server_online() \n"
            + "[ O ]: " + str(response) + '\n'
        )
        self.assertTrue(isinstance(response, dict))
        self.assertFalse(response.get('failed'))
        self.assertEqual(len(response.keys()), 2)
        self.assertTrue(isinstance(response.get('server'), str))
        return response
