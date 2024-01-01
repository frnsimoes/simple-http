class DummyDB:
    users = []

    @classmethod
    def create_user(cls, username):
        cls.users.append(username)
        return username

    @classmethod
    def get_users(cls):
        return cls.users
