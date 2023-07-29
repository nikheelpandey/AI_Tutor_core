import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://nikhil:sZYen1RzqzNB11zG@cluster0.g4lkqmc.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

user_db = client["cluster0"]
collection = user_db["users"]

course_db = client["cluster0"]['courses']

def authenticate_user(username, password):
    # Connect to the MongoDB database
    

    # Retrieve user information from the database based on the username
    user = collection.find_one({"username": username})

    if user:
        # Extract the hashed password from the user document
        hashed_password = user["password"]

        # Verify the provided password against the hashed password
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return True

    return False



def register_user(email, username, password, age, phone):

    # Connect to the MongoDB database
    collection = user_db["users"]

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Create a new user document
    user = {
        "email": email,
        "username": username,
        "password": hashed_password,
        "age": age,
        "phone":phone,
        "courses":[],
        "recent_courses":[],
        "last_course":None
    }

    #check if username is unique
    users = collection.find({"username": username})
    emails =  collection.find({"email": email})
    phs = collection.find({"phone": phone})


    if list(users) or username=="":
        return False, 'username already exists.'

    if list(emails) or email=="":
        return False, 'email already registred.'
    
    if list(phs) or phone=="":
        return False, 'phone no. already registred.'
    

    # Insert the user document into the collection
    collection.insert_one(user)

    return True, 'successfully registered'


def verify(otp, user):
    return True


def getusers(uname):
    users = collection.find({"username": uname})
    return users


if __name__=='__main__':
    ret = getusers('nikhilp')
    print(list(ret))