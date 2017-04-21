import datetime

from feinstrubbot.Command import Command

class CreateUserCommand(Command):
    def __init__(self, users, userID, userName, location, longitude, latitude, chatID):
        print("command created")

        self.users = users
        self.userID = userID
        self.userName = userName
        self.location = location
        self.longitude = longitude
        self.latitude = latitude
        self.chatID = chatID

    def execute(self):
        print("Command executed")
        newUser = {
            "userID": self.userID,
            "userName": self.userName,
            "locations": [
                {
                    "name": self.location,
                    "longitude": self.longitude,
                    "latitude": self.latitude
                }
            ],
            "quietHours": [
                {
                    "start": "22:00",
                    "end": "06:00"
                }
            ],
            "alarmInterval": 5,  # Timeinterval in minutes
            "lastAction": datetime.datetime.utcnow(),
            "chat_id": self.chatID
        }
        self.users.insert_one(newUser)

