import json
import socket
from server_package import server_data
from server_package.menu import CommandHandler
from server_package.functions import SystemUtilities


class Server:
    def __init__(self, srv_host, srv_port, srv_buff):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_buff = srv_buff
        self.handler = CommandHandler()

    def server_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.srv_host, self.srv_port))
            s.listen()
            print("Server started.")
            while True:
                conn, addr = s.accept()
                SystemUtilities.clear_screen()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(self.srv_buff)
                    print(f'Server USER DATA = {data}')
                    result = self.handle_connection(data)
                    conn.sendall(result.encode(server_data.ENCODE_FORMAT))

                    if "Connection" in result:
                        if json.loads(result)["Connection"] == server_data.CLOSE:
                            print("Server stopped")
                            break

    def handle_connection(self, data):
        com = self.json_decode_received_data(data)
        result = self.json_serialize_response(self.handler.use_command(com))
        return result

    @staticmethod
    def json_decode_received_data(received_data):
        decoded_data = json.loads(received_data)
        if 'login' in decoded_data['command']:
            print(f"Command received from Client: login")
            return decoded_data["command"]
        else:
            print(f"Command received from Client: {decoded_data['command']}")
        return decoded_data["command"]

    @staticmethod
    def json_serialize_response(response):
        return json.dumps(response)


def start():
    SystemUtilities.clear_screen()
    server = Server(server_data.HOST, server_data.PORT, server_data.BUFFER_SIZE)
    server.server_connection()


if __name__ == '__main__':
    start()
