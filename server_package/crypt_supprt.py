import bcrypt


class Crypto:

    def password_hashing(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verifying_password(self, stored_hashed_password, provided_password):
        if isinstance(provided_password, str):
            provided_password = provided_password.encode('utf-8')
        if isinstance(stored_hashed_password, str):
            stored_hashed_password = stored_hashed_password.encode('utf-8')
        return bcrypt.checkpw(provided_password, stored_hashed_password)


