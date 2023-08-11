import client


class ServerCommunication:
    @staticmethod
    def send_command(command):
        return client.start(command)
