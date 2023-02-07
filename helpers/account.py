from pymongo.collection import Collection
import requests


def check_if_user_exists(collection: Collection, user: dict) -> bool:
    username = user["username"]
    email = user["email"]
    record = collection.find_one({"email": email})

    if not record:
        return False

    email_status = False
    if email == record["email"]:
        email_status = True

    username_status = False
    if username == record["username"]:
        username_status = True

    if username_status or email_status:
        return True

    return False


def insert_user(collection: Collection, user: dict) -> str or None:
    if not check_if_user_exists(collection, user):
        insertion_result = collection.insert_one(user)
        if not insertion_result.inserted_id:
            return None

        return insertion_result.inserted_id
    else:
        return None


def delete_user(collection: Collection, username: str):
    delete_result = collection.delete_one({"username": username})
    if delete_result.deleted_count == 1:
        return True

    return False


def check_email(email: str) -> bool or None:
    response = requests.get(f"https://www.disify.com/api/email/{email}")
    if response.status_code == 200:
        data = response.json()
        valid_format = data["format"]
        try:
            is_disposable = data["disposable"]
        except KeyError:
            is_disposable = False

        if valid_format and not is_disposable:
            return True

        return False
    else:
        return None
