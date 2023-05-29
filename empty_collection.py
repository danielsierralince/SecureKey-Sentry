from pymongo import MongoClient

#MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["proyectoEd"]
collection = db["otp_collection"]

#My DB
my_host = "localhost"
my_port = 27017
my_uri = f"mongodb://{my_host}:{my_port}"

#DB Access
my_db = "SecureKey-Sentry"
my_collect = "Users"

client = MongoClient(my_uri)
data_base = client[my_db]
collection = data_base[my_collect]

for _ in range(100):
    template = {
        "_id": _,
        "user": None,
        "password hash": "",
        "Cc": "",
        "OTP": 0,
        "active": 0
    }
    collection.insert_one(template)