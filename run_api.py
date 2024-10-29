from server.cache_api import server, set_mongo_client
from pymongo import MongoClient
from waitress import serve
import os

if __name__ == '__main__':
    mongo_client = MongoClient(os.environ["CACHE_MONGODB_URI"])
    set_mongo_client(mongo_client)
    serve(server, host="0.0.0.0", port=5000)
    mongo_client.close()