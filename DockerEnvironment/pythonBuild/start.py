#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient  # MongoDB Library
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import Bot
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import ssl

import googlemaps

import json
from urllib.request import urlopen

import math
import datetime
from time import gmtime, strftime


class Mediator:

    def reactorToResponder(self, message, chat_id):
        self._responder.sendAnswerToClient(self.bot, message,chat_id)


    def __init__(self, users=[], bot=[], gmaps=[]):
        self.users = users
        self.bot = bot
        self.gmaps = gmaps
        self._responder = AntwortSender(self);
        self._reactor = Feinstrubbot(self, users);

        self._reactor.readGoogleToke()
        self._reactor.connectoToGoogle()
        self._reactor.connectToDB()
        self._reactor.readTelegramToken()
        self._reactor.connectToBot()


class AntwortSender:
    def __init__(self, mediator):
        self._mediator = mediator

    def sendAnswerToClient(self, bot, message, chat_id):
        bot.sendMessage(chat_id=chat_id, text=message)

class Feinstrubbot:
    alarm = 0

    #
    # Initialisation
    #
    def readGoogleToke(self):
        fileHandle = open("google.token", "r")
        return fileHandle.readline().strip()

    def connectoToGoogle(self):
        self.gmaps = googlemaps.Client(key=self.readGoogleToke())
        print("Connected to GMaps", self.gmaps)

    def connectToDB(self):
        #client = MongoClient('database', 27017)
        db = self.client.feinstaub
        self.users = db['users']
        print("Connected to DB", self.users)

    def readTelegramToken(self):
        fileHandle = open("bot.token", "r")
        return fileHandle.readline().strip()

    def connectToBot(self):
        print("Connecting to bot")
        telegramToken = token = self.readTelegramToken()
        updater = Updater(token=telegramToken)
        self.bot = Bot(token=telegramToken)

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

    def text(self, bot, update):
        userID = update.message.from_user.id
        user = self.users.find_one({"userID": userID})
        userName = user["userName"]
        text = "No answer"
        if update.message.text == "How is the air quality?":
            self.getAirQuality(userID, userName, bot, update)
        elif update.message.text.startswith("How is the air quality in"):
            split = location = update.message.text.split("How is the air quality in ")
            if len(split) != 2:
                text="Can't get location"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                location = split[1]
                self.getAirQualityFrom(userID, userName, location, bot, update)
        elif update.message.text.startswith("My current location is"):
            split = update.message.text.split("My current location is ")
            if len(split) != 2:
                text=userName + ", I can't get this location"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                location = split[1]
                self.setNewLocation(userID, userName, location, bot, update)
        elif update.message.text == "stats":
            self.getAllLocations(userID, bot, update)
        elif update.message.text == "What are my locations stats?":
            self.getAllLocations(userID, bot, update)
        elif update.message.text.startswith("Add to my locations:"):
            split = location = update.message.text.split("Add to my locations: ")
            if len(split) != 2:
                text=userName + ", I can't get this location"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                location = split[1]
                self.addNewLocation(userID, userName, location, bot, update)
        elif update.message.text.startswith("Remove from my locations:"):
            split = location = update.message.text.split("Remove from my locations: ")
            if len(split) != 2:
                text = userName + ", I can't get this location"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                location = split[1]
                self.removeLocation(userID, location, bot, update)
        elif update.message.text.startswith("Please call me"):
            split = location = update.message.text.split("Please call me ")
            if len(split) != 2:
                text="Sorry, I don't know how to call you!"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                name = split[1]
                self.setNewUserName(userID, userName, name, bot, update)
        elif update.message.text.startswith("Please notify my every"):
            split = location = update.message.text.split("Please notify my every ")
            if len(split) != 2:
                text="Sorry " + userName + ", I don't know when to notify you!"
                self._mediator.reactorToResponder(text, update.message.chat_id)
            else:
                params = split[1]
                params = params.split(" ")
                if len(params) == 1:
                    if params[1] == "h" or params[1] == "hour" or params[1] == "hours":
                        params[0] *= 60

                    self.setAlarmInterval(userID, params[0], bot, update)
                else:
                    text = userName + " please provide a valid time interval. Like '5 min' or '2 hours'. Please keep in mind, that we also the number 1 (1 hour ~ every hour)"
                    self._mediator.reactorToResponder(text, update.message.chat_id)

        elif update.message.text.startswith("Set quiet hours"):
            split = update.message.text.split("Set quiet hours ")
            params = split[1].split(" ")
            if len(params) == 4:
                start = params[1]
                end = params[3]
                self.updateQuietHours(userID, start, end)
                text="Okay " + userName + "! Now I keep calm between " + start + " and " + end + "!"
            else:
                text=userName + " please provide a message in this form: 'Set quiet hours from $start$ to $end$'. $start$/$end$ = 10:00 in 24h-format!"

            self._mediator.reactorToResponder(text, update.message.chat_id)
        elif update.message.text.startswith("debug"):
            user = self.users.find_one({"userID": update.message.from_user.id})
            print(user["locations"])
        elif update.message.text == "What is the alarm status?":
            if self.getAlarmStatus() == 1:
                text="It is Feinstaubalarm in Stuttgart"
            else:
                text="It is no Feinstaubalarm in Stuttgart"
            self._mediator.reactorToResponder(text, update.message.chat_id)

        else:
            text="Hi " + userName + ", what did you mean?!"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="List of Commands:"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="Please call me $name$ - Setup your nickname"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="Remove from my locations: $locationName$ - Removes location"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="Add to my locations: $locationName$ - Add location"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="My current location is $locationName$ - Set default your location"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="How is the air quality in $locationName$ - Returns air-quality from location"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="How is the air quality? - Returns air-quality from default location"
            self._mediator.reactorToResponder(text, update.message.chat_id)
            text="What are my locations stats? - Returns your locations"
            self._mediator.reactorToResponder(text, update.message.chat_id)

    #
    # Helper Functions
    #
    def isfloat(value):
        try:
            float(value)
            return True
        except:
            return False

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    #
    # Location Functions
    #
    def setNewLocation(self, userID, userName, location, bot, update):
        geoResult = self.gmaps.geocode(location)
        if not geoResult:
            self._mediator.reactorToResponder( "Can't find location", update.message.chat_id)
        else:
            if self.userExists(userID):
                longitude = float(geoResult[0]['geometry']['location']['lng'])
                latitude = float(geoResult[0]['geometry']['location']['lat'])
                self.updateLocation(userID, userName, location, longitude, latitude)
                currentSensor = self.findNextSensorValues(longitude, latitude)
                currentDustValue = currentSensor['sensordatavalues'][0]['value']
                resultText = "Thank you for your location update, " + userName + " \n The current dust pollution at your new location (" + location + ") is: " + currentDustValue + "µg/m³"
                self._mediator.reactorToResponder( resultText, update.message.chat_id)
            else:
                self._mediator.reactorToResponder( "Sorry you are not registered. Please register first.", update.message.chat_id)

    def addNewLocation(self, userID, userName, location, bot, update):
        geoResult = self._mediator.gmaps.geocode(location)
        if not geoResult:
                self._mediator.reactorToResponder( "Can't find location", update.message.chat_id)
        else:
            if self.userExists(userID):
                longitude = float(geoResult[0]['geometry']['location']['lng'])
                latitude = float(geoResult[0]['geometry']['location']['lat'])
                self.insertLocation(userID, location, longitude, latitude)
                currentSensor = self.findNextSensorValues(longitude, latitude)
                currentDustValue = currentSensor['sensordatavalues'][0]['value']
                resultText = "Thank you for your location update, " + userName + " \n The current dust pollution at " + location + " is: " + currentDustValue + "µg/m³"

                self._mediator.reactorToResponder( resultText, update.message.chat_id)
            else:
                self._mediator.reactorToResponder( "Sorry you are not registered. Please register first.", update.message.chat_id)

    def updateLocation(self, userID, userName, location, longitude, latitude):

        user = self.users.find_one({"userID": userID})
        newLocation = user["locations"][0]
        newLocation["longitude"] = longitude
        newLocation["latitude"] = latitude
        newLocation["name"] = location
        user["locations"][0] = newLocation

        self.users.update({"userID": userID}, user)

    def insertLocation(self, userID, location, longitude, latitude):

        user = self.users.find_one({"userID": userID})
        location = {"longitude": longitude, "latitude": latitude, "name": location}
        user["locations"].append(location)

        self.users.update({"userID": userID}, user)

    def removeLocation(self, userID, locationName, bot, update):

        user = self.users.find_one({"userID": userID})
        index = 0
        found = False
        for location in user["locations"]:
            if location["name"] == locationName:
                found = index

            index += 1

        if not found:
            print(locationName + " not registered for user: " + userID)
            self._mediator.reactorToResponder( locationName + " was not registered for you, " + user["userName"] + "!", update.message.chat_id)
        else:
            user["location"].pop(found)

        self.users.update({"userID": userID}, user)
        self._mediator.reactorToResponder( locationName + " removed!", update.message.chat_id)
        self._mediator.reactorToResponder( user["userName"] + " your current available locations are now", update.message.chat_id)

        index = 0
        for location in user["locations"]:
            index += 1
            self._mediator.reactorToResponder( str(index) + ". " + location["name"], update.message.chat_id)

    def getAllLocations(self, userID, bot, update):
        user = self.users.find_one({"userID": userID})
        self._mediator.reactorToResponder( user["userName"] + " your current available locations are:", update.message.chat_id)
        index = 0
        for location in user["locations"]:
            index += 1
            currentSensor = self.findNextSensorValues(location["longitude"], location["latitude"])
            currentDustValue = currentSensor['sensordatavalues'][0]['value']
            self._mediator.reactorToResponder( str(index) + ". " + location["name"] + " = " + currentDustValue + " µg/m³", update.message.chat_id)

    def userHasLocation(self, locations, locationName):
        found = False
        for x in locations:
            if x["name"] == locationName:
                found = x

        return found

    def getUserLocation(self, userID):
        user = self.users.find_one({"userID": userID})
        result = user["locations"][0]

        if result:
            return (result['longitude'], result['latitude'])
        else:
            print("User not found")

    def getUserLocationFrom(self, userID, locationName):
        user = self.users.find_one({"userID": userID})

        if locationName:
            for x in user["locations"]:
                if x["name"] == locationName:
                    result = x
            if not result:
                print("Location" + locationName + " not registered")
        else:
            result = user["locations"][0]

        if result:
            return (result['longitude'], result['latitude'])
        else:
            print("User not found")

    #
    # User Function
    #
    def setNewUserName(self, userID, userName, newName, bot, update):
        if self.userExists(userID):

            self.updateUser(userID, newName)
            resultText = "Ok, now I'm gonna call you " + newName

            self._mediator.reactorToResponder( resultText, update.message.chat_id)
        else:
            self._mediator.reactorToResponder( "Sorry you are not registered. Please register first.", update.message.chat_id)

    def setAlarmInterval(self, userID, interval, bot, update):
        if self.userExists(userID):
            user = self.users.find({"userID": userID})
            user["alarmInterval"] = interval
            self.users.update({"userID": userID}, user)
            self._mediator.reactorToResponder( "Now I'm gonna keep you every " + interval + " min uptodate!", update.message.chat_id)
        else:
            self._mediator.reactorToResponder( "Sorry you are not registered. Please register first.", update.message.chat_id)

    def updateQuietHours(self, userID, start, end):
        user = self.users.find_one({"userID": userID})
        user["quietHours"][0]["start"] = start
        user["quietHours"][0]["end"] = end
        self.users.update({"userID": userID}, user)

    def userExists(self, userID):
        if self.users.find_one({"userID": userID}):
            return True
        return False

    def deleteUser(self, userID):
        result = self.users.delete_many({"userID": userID})
        if result.deleted_count == 1:
            return True
        return False

    def unregister(self, bot, update):
        userID = update.message.from_user.id
        text = ""
        print(userID)
        if self.userExists(userID):
            if self.deleteUser(userID):
                text="You are now unregistered"
            else:
                text="Failed to unregister you from service"
        else:
            text="You are not registered"

        self._mediator.reactorToResponder( text, userID)

    def registration(self, bot, update):
        userID = update.message.from_user.id
        if self.userExists(userID):
            self._mediator.reactorToResponder( "User already registrated", update.message.chat_id)
        else:
            userName = update.message.from_user.first_name
            location = update.message.text.split(' ', 1)[-1]
            geoResult = self._mediator.gmaps.geocode(location)
            longitude = float(geoResult[0]['geometry']['location']['lng'])
            latitude = float(geoResult[0]['geometry']['location']['lat'])

            print(userID, userName, longitude, latitude)
            newUser = {
                "userID": userID,
                "userName": userName,
                "locations": [
                    {
                        "name": location,
                        "longitude": longitude,
                        "latitude": latitude
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
                "chat_id": update.message.chat_id
            }
            insertedID = self.users.insert_one(newUser).inserted_id
            print("new user: ", insertedID)

            currentSensor = self.findNextSensorValues(longitude, latitude)
            currentDustValue = currentSensor['sensordatavalues'][0]['value']

            resultText = "Hi " + userName + "! Thank you for your registration \n The current dust pollution at your location is: " + currentDustValue + "µg/m³"

            self._mediator.reactorToResponder( resultText, update.message.chat_id)

    def updateUser(self, userID, newName):
        user = self.users.find_one({"userID": userID})
        user["userName"] = newName
        self.users.update({"userID": userID}, user)

    def setUserAlert(self, userID, alertID, newTimer):
        user = self.users.find({"userID": userID})
        notifications = user["notifications"]

    #
    # Johannes Alarm
    #
    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            print(start <= x <= end)
            return start <= x <= end
        else:
            print(start <= x or x <= end)
            return start <= x or x <= end

    def check4FeinstaubAlarm(self):
        if self.getAlarmStatus():
            print("Feinstaubalarm")
            if self.alarm == 0:
                for user in self.users.find({}):
                    quiteHours = user["quietHours"]
                    currHour = strftime("%H")
                    currMin = strftime("%M")
                    covered = False
                    for hour in quiteHours:
                        startTime = hour["start"].split(":")
                        endTime = hour["end"].split(":")
                        print(startTime, endTime)
                        start = datetime.time(int(startTime[0]), int(startTime[1]), 0)
                        end = datetime.time(int(endTime[0]), int(endTime[1]), 0)
                        now = datetime.time(int(currHour), int(currMin), 0)
                        nowMin = int(currHour) * 60 + int(currMin)
                        if not self.time_in_range(start, end, now):
                            if (nowMin % user["alarmInterval"]) == 0:
                                self._mediator.reactorToResponder(self._mediator.bot, user["userName"] + ", it is Feinstaubalarm in Stuttgart", user["userID"])
                                self._mediator.reactorToResponder(self._mediator.bot, "The VVS tickets are cheaper now!", user["userID"])
            self.alarm = 1
        else:
            print("Currently no Feinstaubalarm in Stuttgart")
            for user in self.users.find({}):
                quiteHours = user["quietHours"]
                currHour = strftime("%H")
                currMin = strftime("%M")
                covered = False
                for hour in quiteHours:
                    startTime = hour["start"].split(":")
                    endTime = hour["end"].split(":")
                    start = datetime.time(int(startTime[0]), int(startTime[1]), 0)
                    end = datetime.time(int(endTime[0]), int(endTime[1]), 0)
                    now = datetime.time(int(currHour), int(currMin), 0)
                    nowMin = int(currHour) * 60 + int(currMin)
                    if not self.time_in_range(start, end, now):
                        if (nowMin % user["alarmInterval"]) == 0:
                            self._mediator.reactorToResponder(self._mediator.bot, user["userName"] + ", it is NO Feinstaubalarm in Stuttgart", user["userID"])

            self.alarm = 0
        return self.alarm

    def getAlarmStatus(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "http://www.stuttgart.de/feinstaubalarm/"
        soup = BeautifulSoup(urlopen(url, context=ctx), "html.parser")
        data = soup.h1.string
        if data.find("kein") != (-1):
            self.alarm = 1
            return True
        else:
            self.alarm = 0
            return False

    #
    # DataAPI
    #
    def readAllSensorValues(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "https://api.luftdaten.info/static/v2/data.dust.min.json"
        response = urlopen(url, context=ctx)
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

    def getAirQuality(self, userID, userName, bot, update):
        if not self.userExists(userID):
            self._mediator.reactorToResponder( "You are not registrated to this service", update.message.chat_id)
        else:
            userLocation = self.getUserLocation(userID)
            longitude = userLocation[0]
            latitude = userLocation[1]
            currentSensor = self.findNextSensorValues(longitude, latitude)
            currentDustValue = currentSensor['sensordatavalues'][0]['value']
            resultText = "The current dust pollution at your location is: " + currentDustValue + "µg/m³"

            self._mediator.reactorToResponder( resultText, update.message.chat_id)

    def getAirQualityFrom(self, userID, userName, location, bot, update):
        if not self.userExists(userID):
            self._mediator.reactorToResponder( "You are not registrated to this service", update.message.chat_id)
        else:
            userLocation = self.getUserLocationFrom(userID, location)
            longitude = userLocation[0]
            latitude = userLocation[1]
            currentSensor = self.findNextSensorValues(longitude, latitude)
            currentDustValue = currentSensor['sensordatavalues'][0]['value']
            resultText = "The current dust pollution in " + location + " is: " + currentDustValue + "µg/m³"

            self._mediator.reactorToResponder( resultText, update.message.chat_id)

            #
            # Merge
            #


    def alarmstatus(self, bot, update):
        if update.message.text == "What is the alarm status?":
            resultText = ""
            if self.check4FeinstaubAlarm() == 1:
                resultText="It is Feinstaubalarm in Stuttgart"
            else:
                resultText="It is no Feinstaubalarm in Stuttgart"

            self._mediator.reactorToResponder( resultText, update.message.chat_id)

    def __init__(self, mediator, users, scheduler=BackgroundScheduler(), client=MongoClient('database', 27017) ):
        self._mediator = mediator
        self.scheduler = scheduler
        self.client = client
        self.users = users
        scheduler.add_job(self.check4FeinstaubAlarm, 'interval', minutes=1)
        scheduler.start()


def main():
    mediator = Mediator()


if __name__ == '__main__':
    main()
