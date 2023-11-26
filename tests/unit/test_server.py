import unittest
import json
from unittest.mock import patch
from server_package.server import Server


class TestServerInitialization(unittest.TestCase):
    @patch('server_package.server.Server.server_connection')
    def test_initialization(self):
        test_host = "127.0.0.1"
        test_port = 65432
        test_buff = 1024
        server = Server(test_host, test_port, test_buff)
        self.assertEqual(server.srv_host, test_host)
        self.assertEqual(server.srv_port, test_port)
        self.assertEqual(server.srv_buff, test_buff)


class TestDataHandling(unittest.TestCase):
    def test_json_decode_received_data(self):
        test_data = json.dumps({"command": "test_command"}).encode('utf-8')
        decoded_data = Server.json_decode_received_data(test_data)
        self.assertEqual(decoded_data, "test_command")

    def test_json_serialize_response(self):
        test_response = {"status": "success"}
        serialized_response = Server.json_serialize_response(test_response)
        self.assertEqual(json.loads(serialized_response), test_response)


if __name__ == '__main__':
    unittest.main()
