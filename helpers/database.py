from pymongo import MongoClient


def check_if_db_exists(client: MongoClient, database: str) -> bool:
    databases = client.list_database_names()
    if database in databases:
        return True

    return False


def check_if_collection_exists(client: MongoClient, collection: str, _database: str) -> bool:
    database = client.get_database(_database)
    collections = database.list_collection_names()
    if collection in collections:
        return True

    return False


def perform_db_checks(client: MongoClient, collection: str, database: str) -> bool:
    db_exists = check_if_db_exists(client, database)
    collection_exists = check_if_collection_exists(client, collection, database)

    return db_exists and collection_exists
