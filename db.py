from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint
from config.settings import MONGO_URI
client = MongoClient(MONGO_URI)
db=client.daily_text

# db.records.insert_one({'chatID': '123', 'schedule': '17:00'})
# record = db.records.update_one({ 'chatID': '123' }, { '$set' : { 'schedule': '18:00' }})
# record = db.records.find_one({'chatID': '123'})

# print(record)

# Issue the serverStatus command and print the results
# serverStatusResult=db.command("serverStatus")
# pprint(serverStatusResult)