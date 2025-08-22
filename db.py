# db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DB_NAME", "resume_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
