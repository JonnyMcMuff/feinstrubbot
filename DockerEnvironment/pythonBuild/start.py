#!/usr/bin/env python

from pymongo import MongoClient # MongoDB Library
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import logging

import googlemaps

import json
from urllib.request import urlopen

import math
import datetime

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
        client = MongoClient('database', 27017)
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

        registration_handler = CommandHandler('register', self.registration)
        dispatcher.add_handler(registration_handler)

        unregister_handler = CommandHandler('unregister', self.unregister)
        dispatcher.add_handler(unregister_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        dispatcher.add_handler(unknown_handler)

        text_handler = MessageHandler(Filters.text, self.text)
        dispatcher.add_handler(text_handler)

        updater.start_polling()

    def getAirQuality(self, userID, bot, update):
        if not self.userExists(userID):
            bot.sendMessage(chat_id=update.message.chat_id, text="You are not registrated to this service")
        else:
            userLocation = self.getUserLocation(userID)
            longitude = userLocation[0]
            latitude = userLocation[1]
            currentSensor = self.findNextSensorValues(longitude, latitude)
            currentDustValue = currentSensor['sensordatavalues'][0]['value']
            resultText = "The current dust pollution at your location is: " + currentDustValue + "µg/m³"

            bot.sendMessage(chat_id=update.message.chat_id, text=resultText)


    def getUserLocation(self, userID):
        result = self.users.find_one({"userID": userID})
        if result:
            return (result['longitude'], result['latitude'])
        else:
            print("User not found")

    def text(self, bot, update):
        if update.message.text == "How is the air quality?":
            userID = update.message.from_user.id
            self.getAirQuality(userID, bot, update)
        elif update.message.text.startswith("My current location is"):
            split = location = update.message.text.split("My current location is ")
            if len(split) != 2:
                bot.sendMessage(chat_id=update.message.chat_id, text="Can't get location")
            else:
                location = split[1]
                userID = update.message.from_user.id
                userName = update.message.from_user.first_name
                self.setNewLocation(userID, userName, location, bot, update)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="List of Commands: \n -/registration")

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def updateLocation(self, userID, userName, location, longitude, latitude):
        update = {
            "userID": userID,
            "userName": userName,
            "location": location,
            "longitude": longitude,
            "latitude": latitude,
            "lastAction": datetime.datetime.utcnow()
        }
        user = {
            "userID": userID
        }

        self.users.update(user, update)

    def setNewLocation(self, userID, userName, location, bot, update):
        geoResult = self.gmaps.geocode(location)
        if not geoResult:
            bot.sendMessage(chat_id=update.message.chat_id, text="Can't find location")
        else:
            if self.userExists(userID):
                longitude = float(geoResult[0]['geometry']['location']['lng'])
                latitude = float(geoResult[0]['geometry']['location']['lat'])
                self.updateLocation(userID, userName, location, longitude, latitude)
                currentSensor = self.findNextSensorValues(longitude, latitude)
                currentDustValue = currentSensor['sensordatavalues'][0]['value']

                resultText = "Thank you for your location update \n The current dust pollution at your location is: " + currentDustValue + "µg/m³"

                bot.sendMessage(chat_id=update.message.chat_id, text=resultText)
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="Sorry you are not registered. Please register first.")

    def userExists(self, userID):
        if self.users.find_one({"userID": userID}):
            return True
        return False

    def deleteUser(self, userID):
        result = self.users.delete_many({"userID": userID})
        if result.deleted_count == 1:
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

    def unregister(self, bot, update):
        userID = update.message.from_user.id
        if self.userExists(userID):
            if self.deleteUser(userID):
                bot.sendMessage(chat_id=update.message.chat_id, text="You are now unregistered")
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="Failed to unregister you from service")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="You are not registered")

    def registration(self, bot, update):
        userID = update.message.from_user.id
        userName = update.message.from_user.first_name

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
                "userName": userName,
                "location": location,
                "longitude": longitude,
                "latitude": latitude,
                "lastAction": datetime.datetime.utcnow()
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
