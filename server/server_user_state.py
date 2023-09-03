class ServerUserState:
    def __init__(self):
        self.server_logged_in_username = None
        self.server_logged_in_permissions = None

    def set_user_data(self, username, permissions):
        self.server_logged_in_username = username
        self.server_logged_in_permissions = permissions

    def clear_user_data(self):
        self.server_logged_in_username = None
        self.server_logged_in_permissions = None
