import json
import unittest
from server_package.server import Server
import server_package.server_response as server_response



class TestServer(unittest.TestCase):
    def test_handle_connection(self):
        server = Server('127.0.0.1', 65432, 1024)
        test_data = json.dumps({"command": "test_command"}).encode('utf-8')
        result = server.handle_connection(test_data)
        expected_result = "Command not found"
        self.assertIn(expected_result, result)


class TestDataHandling(unittest.TestCase):
    def test_json_decode_received_data(self):
        test_data = json.dumps({"command": "test_command"}).encode('utf-8')
        decoded_data = Server.json_decode_received_data(test_data)
        self.assertEqual(decoded_data, "test_command")

    def test_json_serialize_response(self):
        test_response = {"status": "success"}
        serialized_response = Server.json_serialize_response(test_response)
        self.assertEqual(json.loads(serialized_response), test_response)

    def test_json_serialize_response_Stop_Server(self):
        test_response = {"Connection": "close"}
        serialized_response = Server.json_serialize_response(test_response)
        self.assertEqual(json.loads(serialized_response), test_response)


if __name__ == '__main__':
    unittest.main()
