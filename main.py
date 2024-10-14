from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")  # Use SQLite for quick testing

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Preferences = Column(JSON)

class Restaurant(Base):
    __tablename__ = "restaurants"
    RestaurantID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Address = Column(String(255), nullable=False)
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    CuisineType = Column(String(100))
    PriceRange = Column(String(50))
    Ambiance = Column(String(100))
    Rating = Column(Float, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic schemas
class UserBase(BaseModel):
    Username: str
    Email: EmailStr
    Preferences: Optional[dict] = None

class UserCreate(UserBase):
    Password: str

class User(UserBase):
    UserID: int
    class Config:
        from_attributes = True  # Replaces 'orm_mode'

class RestaurantBase(BaseModel):
    Name: str
    Address: str
    Latitude: float
    Longitude: float
    CuisineType: Optional[str] = None
    PriceRange: Optional[str] = None
    Ambiance: Optional[str] = None
    Rating: Optional[float] = Field(None, ge=0, le=5)

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    RestaurantID: int

    class Config:
        from_attributes = True  # Replaces 'orm_mode'

# FastAPI app
app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User routes
@app.get("/users/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.UserID == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        Username=user.Username, 
        Email=user.Email, 
        PasswordHash=user.Password, 
        Preferences=user.Preferences
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.UserID == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"message": "User deleted successfully"}

# Restaurant routes
@app.get("/restaurants/", response_model=List[Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).all()

@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def read_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.RestaurantID == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.RestaurantID == restaurant_id).first()
    if restaurant:
        db.delete(restaurant)
        db.commit()
    return {"message": "Restaurant deleted successfully"}
