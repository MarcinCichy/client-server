import json
import socket

import client_data


class Client:
    def __init__(self, srv_host, srv_port, srv_buff):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_buff = srv_buff

    def client_connection(self, sentence):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.srv_host, int(self.srv_port)))
                    in_comm = self.input_command(sentence)
                    s.sendall(in_comm)
                    data = s.recv(self.srv_buff)
                    decoded_data = self.json_decode_received_data(data)
                    if decoded_data.values() == client_data.CLOSE:
                        break
                    else:
                        return decoded_data
            except Exception:
                return {"Error": "Unable to connect to server."}

    def input_command(self, command):
        encoded_command = self.json_serialize_command(command).encode(client_data.ENCODE_FORMAT)
        return encoded_command

    @staticmethod
    def json_serialize_command(comm):
        comm_dict = {"command": comm}
        comm_json = json.dumps(comm_dict)
        return comm_json

    @staticmethod
    def json_decode_received_data(data):
        decoded_data = json.loads(data)
        return decoded_data


def start(sentence):
    client = Client(client_data.HOST, client_data.PORT, client_data.BUFFER_SIZE)
    transmit = client.client_connection(sentence)
    return transmit

