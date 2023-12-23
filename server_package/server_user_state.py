class ServerUserState:
    def __init__(self, username=None, permissions=None):
        self.logged_in_username = username
        self.logged_in_permissions = permissions

    def set_user_data(self, username, permissions):
        self.logged_in_username = username
        self.logged_in_permissions = permissions

    def clear_user_data(self):
        self.logged_in_username = None
        self.logged_in_permissions = None
