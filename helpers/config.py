import configparser


def load_config() -> dict:
    config = configparser.ConfigParser()
    config.read("configuration.cfg")

    username = config.get("DATABASE", "USERNAME")
    password = config.get("DATABASE", "PASSWORD")
    database = config.get("DATABASE", "DATABASE")
    collection = config.get("DATABASE", "COLLECTION")

    config = {"username": username, "password": password, "database": database, "collections": collection}
    return config
