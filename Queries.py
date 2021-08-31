# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Import statements
from pymongo import MongoClient
import pprint
import pymongo
import pandas as pd





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Connect to the database as well as insert a single street to warm things up
    client = MongoClient('localhost:27017')
    db = client["WGUProjects"]
    street = {'name': "Street Name"}
    db.StreetData2.insert_one(street)

    # Get the size of the data in bytes
    db.command('collstats', "StreetData2")['size']

    # Get the number of distinct users
    len(db.StreetData2.distinct("created.user"))

    # Get a list of distinct types of data
    db.StreetData2.distinct("type")

    # Get a count of distinct ways
    len(db.StreetData2.distinct("id", {"type": "way"}))

    # Get a count of distinct nodes
    len(db.StreetData2.distinct("id", {"type": "node"}))

    # Print out a list of all nodes
    db.StreetData2.distinct("name", {"type": "node"})

    # What kinds of amenities are there?
    db.StreetData2.distinct("amenity", {"type": "node"})

    # What are the names of different banks in town?
    db.StreetData2.distinct("name", {"amenity": "bank"})

    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
