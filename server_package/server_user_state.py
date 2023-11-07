class ServerUserState:
    def __init__(self):
        self.logged_in_username = None
        self.logged_in_permissions = None

    def set_user_data(self, username, permissions):
        self.logged_in_username = username
        self.logged_in_permissions = permissions

    def clear_user_data(self):
        self.logged_in_username = None
        self.logged_in_permissions = None

    def __str__(self):
        return f"ServerUserState: username={self.logged_in_username }, permissions={self.logged_in_permissions}"
