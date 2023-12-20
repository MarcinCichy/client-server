import json
import socket
from client_package import client_data


class Client:
    def __init__(self, srv_host, srv_port, srv_buff):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_buff = srv_buff

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def client_connection(self, sentence):
        while True:
            try:
                with self.create_socket() as s:
                    s.connect((self.srv_host, int(self.srv_port)))
                    in_comm = self.input_command(sentence)
                    s.sendall(in_comm)
                    data = s.recv(self.srv_buff)
                    decoded_data = self.json_decode_received_data(data)
                    return decoded_data
            except ConnectionError:
                return {"Error": "Unable to connect to server"}

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

