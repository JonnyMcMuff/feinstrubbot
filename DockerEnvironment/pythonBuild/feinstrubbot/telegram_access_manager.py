class TelegramAccessManager:
    def __init__(self):
        self.token_fileHandle = open("bot.token", "r")

    def get_token(self):
        return self.token_fileHandle.readline().strip()
