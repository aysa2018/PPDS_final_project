import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive information from environment variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = db_connection.cursor()
# Query to select ReviewID, RestaurantID, and Comment fields
query = "SELECT ReviewID, RestaurantID, Comment FROM Reviews;"

cursor.execute(query)

# Fetch all rows from the query result
reviews = cursor.fetchall()

# Print the first few rows to confirm the data retrieval
for review in reviews[:5]:  # Print just the first 5 for verification
    review_id, restaurant_id, comment = review
    print(f"ReviewID: {review_id}, RestaurantID: {restaurant_id}, Comment: {comment}")
