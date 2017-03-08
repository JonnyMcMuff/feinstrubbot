#!/usr/bin/env python

from pymongo import MongoClient # MongoDB Library
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import logging

import googlemaps
from datetime import datetime

class Feinstrubbot:
    def __init__(self):
        self.users = []
        self.gmaps = []

    def readGoogleToke(self):
        fileHandle = open("google.token", "r")
        return fileHandle.readline().strip()

    def connectoToGoogle(self):
        self.gmaps = googlemaps.Client(key=self.readGoogleToke())

    def connectToDB(self):
        client = MongoClient('127.0.0.1', 27017)
        db = client['test-database']
        self.users = db['users']

    def readTelegramToken(self):
        fileHandle = open("bot.token", "r")
        return fileHandle.readline().strip()

    def connectToBot(self):
        print("Connecting to bot")
        updater = Updater(token=self.readTelegramToken())
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        registration_handler = CommandHandler('registration', self.registration)
        dispatcher.add_handler(registration_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        dispatcher.add_handler(unknown_handler)

        help_handler = MessageHandler(Filters.text, self.help)
        dispatcher.add_handler(help_handler)

        updater.start_polling()

    def help(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="List of Commands: \n -/registration")

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def userExists(self, userID):
        if self.users.find_one({"userID": userID}):
            return True
        return False

    def registration(self, bot, update):
        userID = update.message.from_user.id
        if self.userExists(userID):
            print("User already in database")
            bot.sendMessage(chat_id=update.message.chat_id, text="You are already registered to the bot")
        else:
            location = update.message.text.split(' ', 1)[-1]
            geoResult = self.gmaps.geocode(location)
            longitude = geoResult[0]['geometry']['location']['lng']
            latitude = geoResult[0]['geometry']['location']['lat']

            newUser = {
                "userID" : userID,
                "location": location,
                "longitude": longitude,
                "latitude": latitude
            }
            insertedID = self.users.insert_one(newUser).inserted_id
            print("new user: ", insertedID)
            bot.sendMessage(chat_id=update.message.chat_id, text="Thank you for your registration")

def main():
    feinstrubbot = Feinstrubbot()
    feinstrubbot.connectoToGoogle()
    feinstrubbot.connectToDB()
    feinstrubbot.connectToBot()

if __name__ == '__main__':
    main()
