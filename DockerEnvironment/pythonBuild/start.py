#!/usr/bin/env python

from pymongo import MongoClient # MongoDB Library
import datetime # used to create a sample document with timestamp
import pprint # pretty printer for the mongodb data

from telegram.ext import Updater
import logging

from telegram.ext import MessageHandler, CommandHandler


class Feinstrubbot:
    def __init__(self):
        self.users = []

    def connectToDB(self):
        client = MongoClient('127.0.0.1', 27017)
        db = client['test-database']
        self.users = db['users']

    def readToken(self):
        fileHandle = open("bot.token", "r")
        return fileHandle.readline().strip()

    def connectToBot(self):
        print("Connecting to bot")
        updater = Updater(token=self.readToken())
        dispatcher = updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        registration_handler = CommandHandler('registration', self.registration)
        dispatcher.add_handler(registration_handler)

        updater.start_polling()

    def userExists(self, userID):
        if self.users.find_one({"userID": userID}):
            return True
        return False

    def registration(self, bot, update):
        userID = update.message.from_user.id
        if self.userExists(userID):
            print("User already in database");
            bot.sendMessage(chat_id=update.message.chat_id, text="You are already registered to the bot")
        else:
            newUser = {
                "userID" : userID
            }
            insertedID = self.users.insert_one(newUser).inserted_id
            print("new user: ", insertedID)
            bot.sendMessage(chat_id=update.message.chat_id, text="Thank you for your registration")

def main():
    feinstrubbot = Feinstrubbot()
    feinstrubbot.connectToDB()
    feinstrubbot.connectToBot()

if __name__ == '__main__':
    main()
