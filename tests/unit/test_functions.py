import unittest

import server_package.server_data
from server_package.server import Server
from server_package.functions import SystemUtilities


class TestServerFunctions(unittest.TestCase):

    def serverUp(self):
        self.server = Server(server_package.server_data.HOST, server_package.server_data.PORT, server_package.server_data.BUFFER_SIZE)
        print("Server startet from TEST")


if __name__ == '__main__':
    unittest.main()


