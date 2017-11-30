from pymongo import MongoClient

client = MongoClient()
db = client.test
cursor = db.numbers.find().sort('date',pymongo.ASCENDING)
for document in cursor:
    print(document["number"])
    print(document["date"])
