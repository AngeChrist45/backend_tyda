import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


load_dotenv()


MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "tyda_database"


client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


# Collections
users_collection = db.users
products_collection = db.products
orders_collection = db.orders
negotiations_collection = db.negotiations
notifications_collection = db.notifications
categories_collection = db.categories