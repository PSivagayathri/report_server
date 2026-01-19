from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from db.connection import users_collection

router = APIRouter()

# Bcrypt maximum password length
MAX_BCRYPT_LENGTH = 72

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(user: User):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Truncate password to avoid bcrypt length error
    safe_password = user.password[:MAX_BCRYPT_LENGTH]

    # Hash password
    hashed_password = bcrypt.hash(safe_password)

    # Insert user into DB
    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    return {"message": "Signup successful!"}

@router.post("/login")
def login(user: LoginUser):
    existing_user = users_collection.find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Truncate password before verifying
    safe_password = user.password[:MAX_BCRYPT_LENGTH]

    if not bcrypt.verify(safe_password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Login successful", "name": existing_user["name"], "email": user.email}
