from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, JSON, BigInteger, DECIMAL, Date, TIMESTAMP, ForeignKey, Float, or_, and_
from sqlalchemy.orm import relationship, joinedload, declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, List 
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fuzzywuzzy import fuzz
import spacy
from neighborhoods import NEIGHBORHOODS

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bistromoods-frontend-886616041508.us-central1.run.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root ():
        return {"status": "backend is running!"}
    
@app.options("/login/")
async def login_options():
    return JSONResponse({"status": "preflight OK"})

#import passlib and set up password hashing

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Database configuration from .env file
DATABASE_URL= "mysql+pymysql://bistromoods:F.iZMuY%27%5E%5EgYhdFG@34.44.42.132:3306/bistromoods"

print(f"DATABASE_URL: {DATABASE_URL}")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# SQLAlchemy model for User
class UserModel(Base):
    __tablename__ = "users" #updated to correct table in database
    
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, index=True, nullable=False)
    Email = Column(String(100), unique=True, index=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)  # hashing
    Preferences = Column(JSON, nullable=True)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the model for login data
class UserLogin(BaseModel):
    Email: str
    Password: str

# POST endpoint for user login
@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Look for the user in the database
    db_user = db.query(UserModel).filter(UserModel.Email == user.Email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Verify the password
    if not pwd_context.verify(user.Password, db_user.PasswordHash):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Return success if credentials are valid
    return {"message": "Login successful"}

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
# SQLAlchemy model for Restaurant
class RestaurantModel(Base):
    __tablename__ = "Restaurants"
    RestaurantID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    Address = Column(String(255), nullable=False)
    CuisineType = Column(String(50), nullable=True)
    PriceRange = Column(String(10), nullable=True)  # Example: $, $$, $$$
    Rating = Column(Float, nullable=True)
    Ambiance = Column(String(100), nullable=True) 
    Latitude = Column(DECIMAL(9, 6), nullable=True)  # Map to database column
    Longitude = Column(DECIMAL(9, 6), nullable=True)
    YelpURL = Column(String(255), nullable=True)
    #Relationdhip with mood table
    moods = relationship("RestaurantMood", back_populates="restaurant")

    

# Pydantic schema for creating a restaurant
class RestaurantCreate(BaseModel):
    Name: str
    Address: str
    CuisineType: Optional[str] = None
    PriceRange: Optional[str] = None
    Rating: Optional[float] = None
    Ambiance: Optional[str] = None

# Pydantic schema for restaurant response
class Restaurant(BaseModel):
    RestaurantID: int
    Name: str
    Address: str
    CuisineType: Optional[str] = None
    PriceRange: Optional[str] = None
    Rating: Optional[float] = None
    Ambiance: Optional[str] = None
    YelpURL: Optional[str] = None
    Latitude: Optional[float] = None  # Ensure these fields are included
    Longitude: Optional[float] = None

    class Config:
        orm_mode = True


# SQLAlchemy model for SearchQueries
class SearchQueries(Base):
    __tablename__ = 'SearchQueries'
    QueryID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(BigInteger, index=True)
    SentimentKeywords = Column(String(255))
    FilterCriteria = Column(JSON)
    SearchDate = Column(TIMESTAMP)
    MoodName = Column(String(255))

# Pydantic schema for creating a new search query
class SearchQueryCreate(BaseModel):
    UserID: int
    SentimentKeywords: Optional[str] = None
    FilterCriteria: Optional[Dict] = None
    MoodName: Optional[str] = None

class SearchQuery(BaseModel):
    QueryID: int
    UserID: int
    SentimentKeywords: Optional[str] = None
    FilterCriteria: Optional[Dict] = None
    SearchDate: Optional[datetime] = None  
    MoodName: Optional[str] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convert datetime to ISO 8601 string
        }

# SQLAlchemy model for Discounts
class Discounts(Base):
    __tablename__ = 'Discounts'
    DiscountID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    RestaurantID = Column(BigInteger, index=True)
    DiscountDescription = Column(String(255))
    DiscountAmount = Column(DECIMAL(5, 2))
    ValidDays = Column(String(100))
    StartDate = Column(Date)
    EndDate = Column(Date)

# Pydantic schema for creating a new discount
class DiscountCreate(BaseModel):
    RestaurantID: int
    DiscountDescription: str
    DiscountAmount: float
    ValidDays: str
    StartDate: date 
    EndDate: date

class Discount(BaseModel):
    DiscountID: int
    RestaurantID: int
    DiscountDescription: str
    DiscountAmount: float
    ValidDays: str
    StartDate: date  
    EndDate: date    

class UserMood(Base):
    __tablename__ = "UserMood"
    
    id = Column(Integer, primary_key=True, index=True)  # Add primary key
    UserID = Column(Integer, ForeignKey("users.UserID"), nullable=False)
    MoodName = Column(String(255), nullable=False)


class UserMoodCreate(BaseModel):
    UserID: int
    MoodName: str

# Pydantic schema for user mood response
class UserMoodResponse(BaseModel):
    UserID: int
    MoodName: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy objects to be returned as Pydantic models


# SQLAlchemy model for RestaurantMood
class RestaurantMood(Base):
    __tablename__ = "RestaurantMood"
    
    id = Column(Integer, primary_key=True, index=True)  # Add primary key
    RestaurantID = Column(Integer, ForeignKey("Restaurants.RestaurantID"), nullable=False)
    MoodName = Column(String(255), nullable=False)
    #Add relationship back to restaurant table
    restaurant = relationship("RestaurantModel", back_populates="moods")

class RestaurantMoodCreate(BaseModel):
    RestaurantID: int
    MoodName: str

# Pydantic schema for restaurant mood response
class RestaurantMoodResponse(BaseModel):
    RestaurantID: int
    MoodName: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy objects to be returned as Pydantic models


# Create all tables in the database
#Base.metadata.create_all(bind=engine)

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

    # Hash the password before saving
    hashed_password = get_password_hash(user.Password)
    
    # Create a new user instance with the hashed password
    new_user = UserModel(
        Username=user.Username,
        Email=user.Email,
        PasswordHash=hashed_password,  # Use the hashed password here
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

# CRUD operations for SearchQueries
@app.post("/restaurants/", response_model=Restaurant)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = RestaurantModel(
        Name=restaurant.Name,
        Address=restaurant.Address,
        CuisineType=restaurant.CuisineType,
        PriceRange=restaurant.PriceRange,
        Rating=restaurant.Rating,
        Ambiance=restaurant.Ambiance
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

@app.get("/restaurants/", response_model=List[Restaurant])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(RestaurantModel).all()

@app.delete("/restaurants/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.RestaurantID == restaurant_id).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted successfully"}


nlp = spacy.load('en_core_web_sm')
# Keyword extraction function
def extract_keywords(user_prompt: str) -> List[str]:
    doc = nlp(user_prompt)
    # Extract relevant keywords (nouns, adjectives, and proper nouns)
    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ('NOUN', 'ADJ', 'PROPN')]
    print(f"Extracted Keywords: {keywords}")  # Debugging statement
    return keywords
def find_neighborhood(latitude, longitude):
    """
    Determines the neighborhood for a given latitude and longitude.

    """
    from neighborhoods import NEIGHBORHOODS  # Import NEIGHBORHOODS dictionary

    for neighborhood, bounds in NEIGHBORHOODS.items():
        # Check if the coordinates fall within the bounds of the neighborhood
        if (bounds["lat_min"] <= latitude <= bounds["lat_max"] and
                bounds["lon_min"] <= longitude <= bounds["lon_max"]):
            return neighborhood.lower()  # Normalize to lowercase for consistent comparison
    return None  # Return None if no matching neighborhood is found


@app.get("/restaurants/search/", response_model=List[Restaurant])
def search_restaurants(
    user_prompt: str,  # User input for search
    neighborhoods: Optional[List[str]] = Query(None, description="List of neighborhoods to filter"),  # Neighborhoods filter
    rating: Optional[float] = Query(None, description="Minimum rating for the restaurant"),  # Rating filter
    price_range: Optional[str] = Query(None, description="Price range like 'Low', 'Medium', 'High'"),  # Price range filter
    dietary_restriction: Optional[str] = Query(None, description="Dietary restriction like 'Vegetarian', 'Vegan', 'Gluten-Free'"),  # Dietary restriction filter
    special_feature: Optional[str] = Query(None, description="Special feature like 'Family Friendly', 'Pet Friendly', 'Outdoor Seating'"),  # Special feature filter
    db: Session = Depends(get_db)  # Dependency injection for database session
):
    """
    Endpoint to search for restaurants based on user input and filters.
    """
    from neighborhoods import NEIGHBORHOODS  # Import NEIGHBORHOODS dictionary

    # Extract keywords from the user input
    keywords = extract_keywords(user_prompt)
    print(f"Extracted Keywords: {keywords}")  # Debugging

    # Base query for restaurants with joined moods for keyword matching
    query = db.query(RestaurantModel).options(joinedload(RestaurantModel.moods))

    # Map user-friendly price range to database values
    price_map = {
        "Low": ["$", "$$"],
        "Medium": ["$$$"],
        "High": ["$$$$"]
    }

    # Apply rating filter if provided
    if rating is not None:
        query = query.filter(RestaurantModel.Rating >= rating)

    # Apply price range filter if provided
    if price_range in price_map:
        query = query.filter(RestaurantModel.PriceRange.in_(price_map[price_range]))

    # Fetch all restaurants matching the base filters
    all_restaurants = query.all()

    # Normalize and process the neighborhoods list
    if neighborhoods:
        # Process each neighborhood separately
        processed_neighborhoods = []
        for neighborhood in neighborhoods:
            # If a single neighborhood contains commas, split it
            if isinstance(neighborhood, str) and "," in neighborhood:
                processed_neighborhoods.extend([n.strip() for n in neighborhood.split(",")])
            else:
                processed_neighborhoods.append(neighborhood)
        
        normalized_neighborhoods = {n.lower().strip() for n in processed_neighborhoods}
        print(f"Neighborhoods for Filtering: {normalized_neighborhoods}")  # Debugging

        # Filter restaurants by neighborhoods
        filtered_restaurants = []
        for restaurant in all_restaurants:
            # Get the neighborhood of the restaurant
            restaurant_neighborhood = find_neighborhood(float(restaurant.Latitude), float(restaurant.Longitude))
            if restaurant_neighborhood and restaurant_neighborhood.lower() in normalized_neighborhoods:
                filtered_restaurants.append(restaurant)
        
        all_restaurants = filtered_restaurants

    # Filter restaurants based on keywords and other criteria
    matching_restaurants = []
    for restaurant in all_restaurants:
        # Check if all keywords match restaurant details
        if all(
            keyword in restaurant.Name.lower() or
            keyword in (restaurant.CuisineType or "").lower() or
            any(keyword in (mood.MoodName or "").lower() for mood in restaurant.moods)
            for keyword in keywords
        ):
            # Check dietary restriction match
            dietary_match = (
                not dietary_restriction or (restaurant.CuisineType and dietary_restriction.lower() in restaurant.CuisineType.lower())
            )

            # Check special feature match
            special_feature_match = (
                not special_feature or any(special_feature.lower() == mood.MoodName.lower() for mood in restaurant.moods)
            )

            # Add restaurant to results if all criteria match
            if dietary_match and special_feature_match:
                matching_restaurants.append(restaurant)

    # Handle no matches
    if not matching_restaurants:
        raise HTTPException(status_code=404, detail="No restaurants match the search criteria")

    return matching_restaurants



# POST endpoint to create a new search query
@app.post("/searchqueries/", response_model=SearchQuery)
def create_search_query(query: SearchQueryCreate, db: Session = Depends(get_db)):
    new_query = SearchQueries(**query.dict())
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

# GET endpoint to retrieve all search queries
@app.get("/searchqueries/", response_model=List[SearchQuery])
def get_search_queries(db: Session = Depends(get_db)):
    return db.query(SearchQueries).all()

# GET endpoint to retrieve a search query by ID
@app.get("/searchqueries/{query_id}", response_model=SearchQuery)
def get_search_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(SearchQueries).filter(SearchQueries.QueryID == query_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")
    return query

# PUT endpoint to update a search query by ID
@app.put("/searchqueries/{query_id}", response_model=SearchQuery)
def update_search_query(query_id: int, query: SearchQueryCreate, db: Session = Depends(get_db)):
    db_query = db.query(SearchQueries).filter(SearchQueries.QueryID == query_id).first()
    if db_query is None:
        raise HTTPException(status_code=404, detail="Search query not found")
    
    # Update the search query fields
    db_query.UserID = query.UserID
    db_query.SentimentKeywords = query.SentimentKeywords
    db_query.FilterCriteria = query.FilterCriteria
    db_query.MoodName = query.MoodName

    db.commit()
    db.refresh(db_query)  # Refresh the instance with the updated data
    return db_query

# DELETE endpoint to delete a search query by ID
@app.delete("/searchqueries/{query_id}")
def delete_search_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(SearchQueries).filter(SearchQueries.QueryID == query_id).first()
    if query is None:
        raise HTTPException(status_code=404, detail="Query not found")
    db.delete(query)
    db.commit()
    return {"message": "Search query deleted successfully"}

# CRUD operations for Discounts

# POST endpoint to create a new discount
@app.post("/discounts/", response_model=Discount)
def create_discount(discount: DiscountCreate, db: Session = Depends(get_db)):
    new_discount = Discounts(**discount.dict())
    db.add(new_discount)
    db.commit()
    db.refresh(new_discount)
    return new_discount

# GET endpoint to retrieve all discounts
@app.get("/discounts/", response_model=List[Discount])
def get_discounts(db: Session = Depends(get_db)):
    return db.query(Discounts).all()

# GET endpoint to retrieve a discount by ID
@app.get("/discounts/{discount_id}", response_model=Discount)
def get_discount(discount_id: int, db: Session = Depends(get_db)):
    discount = db.query(Discounts).filter(Discounts.DiscountID == discount_id).first()
    if discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount

# PUT endpoint to update a discount by ID 
@app.put("/discounts/{discount_id}", response_model=Discount)
def update_discount(discount_id: int, discount: DiscountCreate, db: Session = Depends(get_db)):
    db_discount = db.query(Discounts).filter(Discounts.DiscountID == discount_id).first()
    if db_discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    
    # Update the discount fields
    db_discount.RestaurantID = discount.RestaurantID
    db_discount.DiscountDescription = discount.DiscountDescription
    db_discount.DiscountAmount = discount.DiscountAmount
    db_discount.ValidDays = discount.ValidDays
    db_discount.StartDate = discount.StartDate
    db_discount.EndDate = discount.EndDate

    # Commit the changes to the database
    db.commit()
    db.refresh(db_discount)  # Refresh to get the updated data
    return db_discount

# DELETE endpoint to delete a discount by ID
@app.delete("/discounts/{discount_id}")
def delete_discount(discount_id: int, db: Session = Depends(get_db)):
    discount = db.query(Discounts).filter(Discounts.DiscountID == discount_id).first()
    if discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")
    db.delete(discount)
    db.commit()
    return {"message": "Discount deleted successfully"}


# POST endpoint to create a new user mood
@app.post("/usermoods/")
async def create_user_mood(user_mood: UserMoodCreate, db: Session = Depends(get_db)):
    # Create a new UserMood object with the values from the request
    new_user_mood = UserMood(**user_mood.dict())
    db.add(new_user_mood)
    db.commit()
    db.refresh(new_user_mood)
    return new_user_mood


# GET endpoint to retrieve all user moods
@app.get("/usermoods/", response_model=list[UserMoodResponse])
def get_user_moods(db: Session = Depends(get_db)):
    return db.query(UserMood).all()

# GET endpoint to retrieve moods by user ID
@app.get("/usermoods/{user_id}", response_model=list[UserMoodResponse])
def get_user_moods_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user_moods = db.query(UserMood).filter(UserMood.UserID == user_id).all()
    if not user_moods:
        raise HTTPException(status_code=404, detail="User moods not found")
    return user_moods

# POST endpoint to create a new restaurant mood
@app.post("/restaurantmoods/", response_model=RestaurantMoodResponse)
def create_restaurant_mood(restaurant_mood: RestaurantMoodCreate, db: Session = Depends(get_db)):
    new_restaurant_mood = RestaurantMood(**restaurant_mood.dict())
    db.add(new_restaurant_mood)
    db.commit()
    db.refresh(new_restaurant_mood)
    return new_restaurant_mood

# GET endpoint to retrieve all restaurant moods
@app.get("/restaurantmoods/", response_model=list[RestaurantMoodResponse])
def get_restaurant_moods(db: Session = Depends(get_db)):
    return db.query(RestaurantMood).all()

# GET endpoint to retrieve moods by restaurant ID
@app.get("/restaurantmoods/{restaurant_id}", response_model=list[RestaurantMoodResponse])
def get_restaurant_moods_by_restaurant_id(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant_moods = db.query(RestaurantMood).filter(RestaurantMood.RestaurantID == restaurant_id).all()
    if not restaurant_moods:
        raise HTTPException(status_code=404, detail="Restaurant moods not found")
    return restaurant_moods

class ReviewModel(Base):
    __tablename__ = "Reviews"  # Matching to table in database

    ReviewID = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    RestaurantID = Column(BigInteger, ForeignKey("restaurants.RestaurantID"), nullable=False)
    UserID = Column(BigInteger, ForeignKey("users.UserID"), nullable=False)
    Rating = Column(DECIMAL(2, 1), nullable=False)
    Comment = Column(String(1000), nullable=False)
    ReviewDate = Column(TIMESTAMP, server_default=func.now())


class ReviewCreate(BaseModel):
    RestaurantID: int
    UserID: int
    Rating: float
    Comment: str

class Review(BaseModel):
    ReviewID: int
    RestaurantID: int
    UserID: int
    Rating: float
    Comment: str
    ReviewDate: datetime

    class Config:
        orm_mode = True

@app.get("/restaurants/", response_model=List[Restaurant])
def get_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(RestaurantModel).all()
    for restaurant in restaurants:
        print(f"Name: {restaurant.Name}, Latitude: {restaurant.Latitude}, Longitude: {restaurant.Longitude}")
    return restaurants

# POST endpoint to create a new review
@app.post("/reviews/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_review = ReviewModel(
        RestaurantID=review.RestaurantID,
        UserID=review.UserID,
        Rating=review.Rating,
        Comment=review.Comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# GET endpoint to retrieve all reviews for a specific restaurant
@app.get("/restaurants/{restaurant_id}/reviews/", response_model=List[Review])
def get_reviews_for_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.RestaurantID == restaurant_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this restaurant")
    return reviews

# PUT endpoint to update a review by ID
@app.put("/reviews/{review_id}", response_model=Review)
def update_review(review_id: int, updated_review: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.ReviewID == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    review.Rating = updated_review.Rating
    review.Comment = updated_review.Comment
    db.commit()
    db.refresh(review)
    return review

# DELETE endpoint to delete a review by ID
@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.ReviewID == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
