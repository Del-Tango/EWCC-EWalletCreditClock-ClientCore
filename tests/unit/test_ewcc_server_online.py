import unittest

from ewcc_lib import ewallet_client


class TestEwalletClientServerOnline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.core = ewallet_client.EWalletClientCore()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_ewcc_server_online_unit(self):
        print('[ * ]: EWCC Subroutine ServerOnline -')
        self.core.config_reload(self.core.config_file)
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
