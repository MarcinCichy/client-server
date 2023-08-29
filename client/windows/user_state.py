class UserState:
    def __init__(self):
        self.login_username = None
        self.login_permissions = None

    def set_user(self, username, permissions):
        self.login_username = username
        self.login_permissions = permissions

    def get_user(self):
        return self.login_username, self.login_permissions
