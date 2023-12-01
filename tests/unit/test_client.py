import json
import unittest
from client_package.client import Client
import server_package.server_response as server_response


class TestClientInitialization(unittest.TestCase):
    def test_initialization(self):
        test_host = "127.0.0.1"
        test_port = 8000
        test_buff = 1024
        client = Client(test_host, test_port, test_buff)
        self.assertEqual(client.srv_host, test_host)
        self.assertEqual(client.srv_port, test_port)
        self.assertEqual(client.srv_buff, test_buff)


class TestClient(unittest.TestCase):
    def test_handle_connection_unrecognised_command(self):
        client = Client('127.0.0.1', 65432, 1024)
        result = client.client_connection({"command": "test_command"})
        expected_result = server_response.UNRECOGNISED_COMMAND
        self.assertEqual(result, expected_result)

    def test_handle_connection_valid_command(self):
        client = Client('127.0.0.1', 65432, 1024)
        result = client.client_connection({"command": "info"})
        expected_result = "version"
        self.assertIn(expected_result, result)
