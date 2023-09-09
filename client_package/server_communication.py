import client
from windows.handlers import Handlers


class ServerCommunication:
    def __init__(self):
        self.handler = Handlers(self)

    @staticmethod
    def send_command(command): 
        return client.start(command)
