class GoogleTokenAccessManager:
    def __init__(self):
        self.token_fileHandle = open("google.token", "r")

    def get_token(self):
        return self.token_fileHandle.readline().strip()