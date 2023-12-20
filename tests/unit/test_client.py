import json
import unittest
from client_package.client import Client
import server_package.server_response as server_response
import server_package.server_data as server_data


class TestClientInitialization(unittest.TestCase):
    def test_initialization(self):
        test_host = "127.0.0.1"
        test_port = 65432
        test_buff = 1024
        client = Client(test_host, test_port, test_buff)
        self.assertEqual(client.srv_host, test_host)
        self.assertEqual(client.srv_port, test_port)
        self.assertEqual(client.srv_buff, test_buff)


# class TestClient(unittest.TestCase):
#     def test_handle_connection_unrecognised_command(self):
#         client = Client('127.0.0.1', 65432, 1024)
#         result = client.client_connection({"username": {"command": "test_command"}})
#         expected_result = server_response.UNRECOGNISED_COMMAND
#         self.assertEqual(result, expected_result)
#
#     def test_handle_connection_valid_command(self):
#         client = Client('127.0.0.1', 65432, 1024)
#         result = client.client_connection({"command": "info"})
#         expected_result = "version"
#         self.assertIn(expected_result, result)


class TestDataHandling(unittest.TestCase):
    def test_json_decode_received_data(self):
        test_data = json.dumps({"version": server_data.VERSION, "start_at": str(server_data.DATE)}).encode('utf-8')
        decoded_data = Client.json_decode_received_data(test_data)
        self.assertIn("version", decoded_data)

    def test_json_serialize_command(self):
        test_command = "test_command"
        serialized_command = Client.json_serialize_command(test_command)
        self.assertEqual(json.loads(serialized_command), {"command": test_command})

    def test_json_serialize_response_Stop_Server(self):
        test_response = {"Connection": "close"}
        serialized_response = Client.json_serialize_command(test_response)
        self.assertEqual(json.loads(serialized_response), {'command': test_response})


if __name__ == "__main__":
    unittest.main(verbosity=2)