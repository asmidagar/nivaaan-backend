# routes/auth_routes.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from database import users_collection
from models.user_model import UserRegister, UserLogin
from utils.jwt_handler import create_token
import bcrypt

router = APIRouter()


# -----------------------------------------------
# 📌 POST /api/auth/register
# Called by: Register.js
# Expects:  { name, email, password }
# Returns:  { message: "Registration successful" }
# -----------------------------------------------
@router.post("/register")
async def register(user: UserRegister):

    # 1. Check if email already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2. Hash password using bcrypt directly
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # 3. Build user document for MongoDB
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    # 4. Insert into MongoDB
    users_collection.insert_one(new_user)

    return {"message": "Registration successful! You can now log in."}


# -----------------------------------------------
# 📌 POST /api/auth/login
# Called by: Login.js
# Expects:  { email, password }
# Returns:  { token: "jwt_token_here" }
# -----------------------------------------------
@router.post("/login")
async def login(credentials: UserLogin):

    # 1. Find user by email
    user = users_collection.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 2. Verify password using bcrypt directly
    is_valid = bcrypt.checkpw(
        credentials.password.encode('utf-8'),
        user["password"].encode('utf-8')
    )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # 3. Generate JWT token
    token = create_token({
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"]
    })

    # 4. Return token
    return {"token": token}

# Add this at the bottom of auth_routes.py

from database import users_collection
from bson import ObjectId


# -----------------------------------------------
# GET /api/auth/users
# Returns all registered users
# -----------------------------------------------
@router.get("/users")
async def get_all_users():
    try:
        users = []
        for user in users_collection.find():
            # Count complaints for each user
            from database import complaints_collection
            complaint_count = complaints_collection.count_documents(
                {"filed_by": str(user["_id"])}
            )
            users.append({
                "id": str(user["_id"]),
                "name": user.get("name", ""),
                "email": user.get("email", ""),
                "complaints": complaint_count
            })
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))