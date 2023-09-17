import client
# from windows.handlers import Handlers


class ClientCommunication:
    def __init__(self):
        pass
        # self.handler = Handlers(self)

    @staticmethod
    def send_command(command): 
        return client.start(command)
