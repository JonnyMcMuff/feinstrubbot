#!/usr/bin/env python

from pymongo import MongoClient # MongoDB Library
import logging
import sys
from terminaltables import AsciiTable
import datetime

class adminTerminal:

    def __init__(self):
        self.users = []
        self.gmaps = []

    def connectToDB(self):
        client = MongoClient('database', 27017)
        db = client['feinstaub']
        self.users = db['users']

    def printAllUsers(self):
        tableData = []
        tableData.append(["id", "name", "locations", "last active"])
        for user in self.users.find({}):
            tableData.append([user['userID'],user['userName'],user['locations'],user['lastAction']])

        table = AsciiTable(tableData)
        print(table.table)

    def removeUsers(self):
        if len(sys.argv) > 1:
            olderThan = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%d')
            result = self.users.delete_many({'lastAction':{ '$lt' : olderThan} })
            print("\ndeleted {} users\nnew table of users:\n".format(result.deleted_count))
            self.printAllUsers()
        else:
            print("date needed to specify which users to delete")

def main():
    terminal = adminTerminal()
    terminal.connectToDB()
    terminal.printAllUsers()
    terminal.removeUsers()

if __name__ == '__main__':
    main()
