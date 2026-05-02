# database.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
load_dotenv()

# -----------------------------------------------
# 🔧 Configuration
# -----------------------------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = "nivaaan"


# -----------------------------------------------
# ✅ Connect to MongoDB
# -----------------------------------------------
try:

    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)

    # Test connection immediately
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")

except ConnectionFailure:
    print("❌ MongoDB connection failed. Is MongoDB running?")


# -----------------------------------------------
# ✅ Database
# -----------------------------------------------
db = client[DB_NAME]


# -----------------------------------------------
# ✅ Collections
# Used directly in routes:
#   → auth_routes.py      uses users_collection
#   → complaint_routes.py uses complaints_collection
# -----------------------------------------------
users_collection      = db["users"]
complaints_collection = db["complaints"]


# -----------------------------------------------
# ✅ Indexes (performance + uniqueness)
# -----------------------------------------------

# Prevent duplicate emails at DB level
users_collection.create_index("email", unique=True)

# Speed up status filter queries (used in summary)
complaints_collection.create_index("status")

# Speed up user-specific complaint lookups
complaints_collection.create_index("filed_by")

print("✅ Database indexes created!")

# database.py — add these 2 lines at the bottom

vendors_collection = db["vendors"]
vendors_collection.create_index("name")