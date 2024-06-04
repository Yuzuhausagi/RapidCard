import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("localhost", 27017)
db = client.words
japaneseAnswer = [
    {"車": "car"},
    {"上": "up"},
    {"下": "down"},
    {"侍": "samurai"},
    {"家族": "family"},
    {"右": "right"},
    {"左": "left"},
    {"恋人": "lover"},
    {"炎": "flame"},
    {"銀行": "bank"},
]


simple_words = [
    "apple",
    "ball",
    "cat",
    "dog",
    "egg",
    "fish",
    "goat",
    "hat",
    "ice",
    "juice",
    "kite",
    "lion",
    "mouse",
    "nut",
    "orange",
    "pig",
    "queen",
    "rose",
    "sun",
    "tree",
    "umbrella",
    "vase",
    "water",
    "x-ray",
    "yarn",
    "zebra",
]

japanese1 = db.Japanese_Answer.insert_many(japaneseAnswer)

for i, w in enumerate(simple_words):
    db.false_words.insert_one({str(i): w}).inserted_id


def grab_amount_of_words(n):
    collection = db["Japanese_Answer"]
    for i in collection.find():
        print(i)


print(grab_amount_of_words(3))
