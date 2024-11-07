# models.py
from sqlalchemy import Column, Integer, String, Text, BIGINT, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Initialize SQLAlchemy base class
Base = declarative_base()

# Define the Reviews model
class Reviews(Base):
    __tablename__ = 'reviews'
    ReviewID = Column(Integer, primary_key=True, autoincrement=True)
    RestaurantID = Column(BIGINT, ForeignKey('restaurants.RestaurantID'), nullable=False)
    UserID = Column(BIGINT, nullable=False)
    Rating = Column(DECIMAL(2, 1), nullable=False)
    Comment = Column(Text)
    ReviewDate = Column(TIMESTAMP, default=datetime.utcnow)
