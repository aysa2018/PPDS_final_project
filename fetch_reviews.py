#Code by Aysa. Please dont edit anything.
import mysql.connector
from dotenv import load_dotenv
import os
import openai


# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
# Set the OpenAI API key
openai.api_key = openai_api_key

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
# for review in reviews[:5]:  # Print just the first 5 for verification
#     review_id, restaurant_id, comment = review
#     print(f"ReviewID: {review_id}, RestaurantID: {restaurant_id}, Comment: {comment}")

# Function to extract keywords using OpenAI API
def extract_keywords(comment):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Extract keywords from the following restaurant review: {comment}"}
        ],
        max_tokens=50,
        temperature=0.3,
    )
    keywords = response.choices[0].message['content'].strip()
    return keywords


# Process each review and extract keywords
for review in reviews:
    review_id, restaurant_id, comment = review
    keywords = extract_keywords(comment)
    print(f"ReviewID: {review_id}, RestaurantID: {restaurant_id}, Keywords: {keywords}")

# Extract and insert keywords
insert_query = "INSERT INTO RestaurantMood (RestaurantID, MoodName) VALUES (%s, %s)"

for review in reviews:
    review_id, restaurant_id, comment = review
    keywords = extract_keywords(comment)

    # Insert each keyword into RestaurantMood
    for keyword in keywords.split(", "):  # Adjust if necessary
        cursor.execute(insert_query, (restaurant_id, keyword))

# Commit changes before closing
db_connection.commit()



# Close the database connection
cursor.close()
db_connection.close()

