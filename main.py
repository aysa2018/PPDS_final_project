from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Database configuration from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for User
class UserModel(Base):
    __tablename__ = "users"

    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, index=True, nullable=False)
    Email = Column(String(100), unique=True, index=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)  # You should hash passwords!
    Preferences = Column(JSON, nullable=True)

# Pydantic schema for creating a new user
class UserCreate(BaseModel):
    Username: str
    Email: EmailStr
    Password: str
    Preferences: Optional[Dict] = None

# Pydantic schema for user response
class User(BaseModel):
    UserID: int
    Username: str
    Email: EmailStr
    Preferences: Optional[Dict] = None

    class Config:
        from_attributes = True  # Allows SQLAlchemy objects to be returned as Pydantic models

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST endpoint to create a new user
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username already exists
    db_user = db.query(UserModel).filter(UserModel.Username == user.Username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create a new user instance
    new_user = UserModel(
        Username=user.Username,
        Email=user.Email,
        PasswordHash=user.Password,  # You should hash the password here in production!
        Preferences=user.Preferences
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Fetch the new user with UserID
    return new_user

# GET endpoint to retrieve all users
@app.get("/users/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users

# DELETE endpoint to delete a user by ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.UserID == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
