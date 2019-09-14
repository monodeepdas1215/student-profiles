from pymongo import MongoClient
from app.utils.config_access import config


class MongoConnection(object):

    _CONNECTION = None

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        if MongoConnection._CONNECTION is None:
            MongoConnection._CONNECTION = MongoClient(config['DB_HOST'], int(config['DB_PORT']))

        return MongoConnection._CONNECTION

    @staticmethod
    def get_database():
        connection = MongoConnection.get_connection()
        return connection[config['DB']]

    @staticmethod
    def get_students_data_collection():
        db = MongoConnection.get_database()
        return db[config['DB_STUDENTS_DATA_COLLECTION']]

    @staticmethod
    def get_students_collection():
        db = MongoConnection.get_database()
        return db[config['DB_STUDENTS_COLLECTION']]

    @staticmethod
    def get_users_collection():
        db = MongoConnection.get_database()
        return db[config['DB_USERS_COLLECTION']]