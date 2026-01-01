from pymongo import MongoClient
import os

db_uri = os.getenv("MONGO_HOST")

class Singelton:
    _instance = None
    @staticmethod
    def get_connection_to_mongo():
        if not Singelton._instance:
            client = MongoClient(f"mongodb://{db_uri}:27017")
            Singelton._instance = 1
            return client


class Connector:
    @staticmethod    
    def get_database(client):
        database = client['contacts_db']
        return database
    

    @staticmethod
    def get_collection(database):
        collection = database['contacts']
        return collection


    

