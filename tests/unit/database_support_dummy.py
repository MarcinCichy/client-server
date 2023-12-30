class DatabaseSupportDummy:
    def __init__(self):
        self.users_data = {"users":
            {
                "RECIPIENT": {
                    "password": "pass",
                    "permissions": "user",
                    "status": "active",
                    "activation_date": "2023-04-06"
                },
                "other_user": {
                    "password": "pass2",
                    "permissions": "admin",
                    "status": "banned",
                    "activation_date": "2023-04-06"
                },
                "logged_username": {
                    "password": "pass3",
                    "permissions": "admin",
                    "status": "active",
                    "activation_date": "2023-04-06"
                }
            },
            "logged_users": [
                "username_invalid",
                "logged_username"
    ]
        }
        self.messages_data = {'messages':
            {
                'RECIPIENT': {
                    "1": {'sender': 'user2', 'date': '2023-01-01', 'content': 'Hello'},
                    "2": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'},
                    "3": {'test_message_3'}
                },
                'FULL_INBOX_USER': {
                    "1": {'sender': 'user2', 'date': '2023-01-01', 'content': 'Hello'},
                    "2": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'},
                    "3": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'},
                    "4": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'},
                    "5": {'sender': 'user3', 'date': '2023-01-02', 'content': 'Hi'},
                },
                'NO_MSGS_USER': {
                },
                "other_user": {

                }
            }
        }

    def get_user(self):
        return self.users_data

    def save_user(self, data):
        self.users_data = data

    def get_messages(self):
        return self.messages_data

    def save_messages(self, data):
        self.messages_data = data


