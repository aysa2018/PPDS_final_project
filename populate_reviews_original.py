import requests
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Yelp API setup
#API_KEY = os.getenv("YELP_API_KEY")
API_KEY="G4u_kUc5wRsLGPw2R-27XnGBirwGF-fJxjRn5jDOegSKmcmtdC93P9OfBddYstaPSW_aE065hJea3wCo4d-DlTXSacWGv9Is-YBel6xTMTX6Qv0DDg-pEJMzZ6YqZ3Yx"
headers = {"Authorization": f"Bearer {API_KEY}"}
reviews_url_template = "https://api.yelp.com/v3/businesses/{}/reviews"

# Database setup
DATABASE_URL="mysql+pymysql://bistromoods:F.iZMuY%27%5E%5EgYhdFG@34.44.42.132:3306/bistromoods"
#DATABASE_URL = os.getenv("DATABASE_URL")
engine = db.create_engine(DATABASE_URL)
metadata = db.MetaData()
restaurants_table = db.Table('Restaurants', metadata, autoload_with=engine)
reviews_table = db.Table('Reviews', metadata, autoload_with=engine)
Session = sessionmaker(bind=engine)
session = Session()

# Loop through restaurants in the database and fetch their reviews
restaurants = session.query(restaurants_table).all()

for restaurant in restaurants:
    # Ensure the Yelp URL contains '/biz/' to extract the business ID
    yelp_url = restaurant.YelpURL
    if '/biz/' in yelp_url:
        business_id = yelp_url.split('/biz/')[1].split('?')[0]  # Extracts just the business ID
        print(f"Fetching up to 3 reviews for {restaurant.Name} with Yelp Business ID: {business_id}")

        # Build the Yelp API URL for fetching reviews
        reviews_url = reviews_url_template.format(business_id)
        print(f"Fetching reviews from URL: {reviews_url}")  # Print URL for debugging
        
        try:
            response = requests.get(reviews_url, headers=headers)
            
            if response.status_code == 200:
                reviews_data = response.json().get('reviews', [])
                for review in reviews_data:
                    review_entry = {
                        'RestaurantID': restaurant.RestaurantID,
                        'UserID': None,  # Adjust based on your schema for UserID if necessary
                        'Rating': review['rating'],
                        'Comment': review['text'],
                        'ReviewDate': review['time_created']
                    }
                    # Insert review into Reviews table
                    insert_stmt = db.insert(reviews_table).values(review_entry)
                    session.execute(insert_stmt)
                    print(f"Inserted review for: {restaurant.Name}")
            else:
                print(f"Failed to fetch reviews for {restaurant.Name}. Error: {response.status_code} {response.reason}")
                print(f"Full response: {response.json()}")  # Print response for more details

        except requests.exceptions.RequestException as e:
            print(f"Error fetching reviews for {restaurant.Name}: {e}")
        
        # Add a delay to avoid rate limiting
        time.sleep(1)
    else:
        print(f"Skipping {restaurant.Name} as its Yelp URL does not contain '/biz/'")

# Commit the transaction and close the session
session.commit()
session.close()