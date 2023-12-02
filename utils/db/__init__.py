from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://mongo:Gfe5a52hHhFgD6aF65CH4acafdGFFA33@monorail.proxy.rlwy.net:39683"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.bot

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
