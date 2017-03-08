#!/usr/bin/env python

from pymongo import MongoClient # MongoDB Library
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import logging

import googlemaps

import json
from urllib.request import urlopen

import math

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

    def readAllSensorValues(self):
        url = "https://api.luftdaten.info/static/v2/data.dust.min.json"
        response = urlopen(url)
        html = response.read().decode('utf-8')
        data = json.loads(html)
        return data

    def findNextSensorValues(self, longitude, latitude):
        data = self.readAllSensorValues()
        minDistance = 99999999999
        for item in data:
            currentLongitude = float(item['location']['longitude'])
            currentLatitude = float(item['location']['latitude'])
            currentDistance = math.pow(currentLongitude - longitude, 2) + math.pow(currentLatitude - latitude, 2)
            if currentDistance < minDistance:
                minDistance = currentDistance
                currentSensor = item
        return currentSensor

    def registration(self, bot, update):
        userID = update.message.from_user.id
        if self.userExists(userID):
            print("User already in database")
            bot.sendMessage(chat_id=update.message.chat_id, text="You are already registered to the bot")
        else:
            location = update.message.text.split(' ', 1)[-1]
            geoResult = self.gmaps.geocode(location)
            longitude = float(geoResult[0]['geometry']['location']['lng'])
            latitude = float(geoResult[0]['geometry']['location']['lat'])

            newUser = {
                "userID" : userID,
                "location": location,
                "longitude": longitude,
                "latitude": latitude
            }
            insertedID = self.users.insert_one(newUser).inserted_id
            print("new user: ", insertedID)

            currentSensor = self.findNextSensorValues(longitude, latitude)
            currentDustValue = currentSensor['sensordatavalues'][0]['value']

            resultText = "Thank you for your registration \n The current dust pollution at your location is: "  + currentDustValue + "µg/m³"

            bot.sendMessage(chat_id=update.message.chat_id, text=resultText)

def main():
    feinstrubbot = Feinstrubbot()
    feinstrubbot.connectoToGoogle()
    feinstrubbot.connectToDB()
    feinstrubbot.connectToBot()

if __name__ == '__main__':
    main()
