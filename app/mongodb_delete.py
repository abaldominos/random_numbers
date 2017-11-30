from pymongo import MongoClient

client = MongoClient()
db = client.test
result = db.numbers.delete_many({})
