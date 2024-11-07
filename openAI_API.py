import os
from dotenv import load_dotenv
import openai
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Reviews, RestaurantMoods

#setting up tthe API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Test the connection with a simple print to confirm the API key is loaded
print("OpenAI API Key Loaded:", openai.api_key is not None)

# Function to extract keywords from review text using OpenAI
def extract_keywords(review_text):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Extract keywords describing the vibe or ambiance of this review: '{review_text}'. Return the keywords only.",
        max_tokens=10,
        temperature=0.5
    )
    keywords = response.choices[0].text.strip().split(", ")
    return keywords