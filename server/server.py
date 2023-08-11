import json
import socket
import srv_datas
import menu
from functions import SystemUtilities


class Server:
    def __init__(self, srv_host, srv_port, srv_buff):
        self.srv_host = srv_host
        self.srv_port = srv_port
        self.srv_buff = srv_buff

    def server_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.srv_host, self.srv_port))
            s.listen()
            print("Server started.")
            print("-" * 17)
            while True:
                conn, addr = s.accept()
                SystemUtilities.clear_screen()
                with conn:
                    print(f"Connected by {addr}")
                    command = conn.recv(self.srv_buff)
                    com = self.decode_received_data(command)
                    result = menu.handler.use_command(com)
                    conn.sendall(result.encode(srv_datas.ENCODE_FORMAT))

                    if "Connection" in result:
                        if (json.loads(result))["Connection"] == srv_datas.CLOSE:
                            print("Server stopped")
                            break

    @staticmethod
    def decode_received_data(received_data):
        if received_data is None:
            SystemUtilities.unrecognised_command()
        else:
            decoded_data = json.loads(received_data)
            if 'login' in decoded_data['command']:
                print(f"Command received from Client: login")  # to hide showing login and password
                return decoded_data["command"]
            else:
                print(f"Command received from Client: {decoded_data['command']}")
            return decoded_data["command"]


def start():
    SystemUtilities.clear_screen()
    server = Server(srv_datas.HOST, srv_datas.PORT, srv_datas.BUFFER_SIZE)
    server.server_connection()


start()
