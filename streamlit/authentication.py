import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://nikhil:sZYen1RzqzNB11zG@cluster0.g4lkqmc.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["cluster0"]


def authenticate_user(username, password):
    # Connect to the MongoDB database
    collection = db["users"]

    # Retrieve user information from the database based on the username
    user = collection.find_one({"username": username})

    if user:
        # Extract the hashed password from the user document
        hashed_password = user["password"]

        # Verify the provided password against the hashed password
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return True

    return False



def register_user(email, username, password, age):
    # Connect to the MongoDB database
    collection = db["users"]

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Create a new user document
    user = {
        "email": email,
        "username": username,
        "password": hashed_password,
        "age": age
    }
    # print(user)
    # Insert the user document into the collection
    collection.insert_one(user)

    return True