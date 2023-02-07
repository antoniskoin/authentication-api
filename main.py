import pymongo
from flask import Flask, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from waitress import serve
from helpers.account import insert_user, delete_user, check_email
from helpers.database import perform_db_checks
from helpers.config import load_config

config = load_config()
app = Flask(__name__)
client = pymongo.MongoClient(
    f"mongodb+srv://{config['username']}:{config['password']}@cluster0.stl7rpk.mongodb.net/?retryWrites=true&w=majority")
result = perform_db_checks(client, config["collections"], config["database"])
if not result:
    print("Database or collection doesn't exist")
    exit()
else:
    print("Database checks completed!")
    database = client.get_database("authentication")


@app.route("/")
def index():
    return redirect("https://github.com/antoniskoin/authentication-api")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if (not username) or (not password) or (not email):
        return {"error": "Please provide all required parameters"}

    hashed_password = generate_password_hash(password)
    data = {"username": username, "password": hashed_password, "email": email}
    collection = database.get_collection("accounts")
    user_id = insert_user(collection, data)
    if user_id:
        return {"user_id": str(user_id)}

    return {"user_id": "user already exists"}


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if (not username) or (not password):
        return {"error": "Please provide all required parameters"}

    record = database.get_collection("accounts")
    user = record.find_one({"username": username})
    db_password = user["password"]
    if check_password_hash(db_password, password):
        return {"success": True}

    return {"success": False}


@app.route("/delete", methods=["POST"])
def delete():
    username = request.form.get("username")
    collection = database.get_collection("accounts")
    deletion_result = delete_user(collection, username)
    return {"success": deletion_result}


@app.route("/validate-email", methods=["POST"])
def email_validation():
    email = request.form.get("email")
    is_valid = check_email(email)
    return {"is_valid": is_valid}


if __name__ == "__main__":
    serve(app)
