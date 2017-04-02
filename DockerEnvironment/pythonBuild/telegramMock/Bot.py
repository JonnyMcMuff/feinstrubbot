class Bot:
    """
    This class should mock the telegram bot module
    It offers function to sendMessages to the bot and to get the
    message that was sent as last
    """
    def __init__(self):
        self.text = None
        self.chat_id = None
        self.messages = []

    def sendMessage(self, chat_id, text):
        if not (self.chat_id is None or self.text is None):
            self.messages.append((self.chat_id, self.text))
        self.chat_id = chat_id
        self.text = text


    def get_last_message(self):
        return self.chat_id, self.text
