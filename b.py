import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["words"]

collection = db["Japanese_Answer"]

data = collection.find()
for i in data:
    print(i)
