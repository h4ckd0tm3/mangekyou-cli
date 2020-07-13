class Credentials:
    username: str
    password: str

    def __init__(self):
        pass

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password