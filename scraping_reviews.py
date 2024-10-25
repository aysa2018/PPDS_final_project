import googlemaps
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

# Google Places API key
API_KEY = ''

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key=API_KEY)

# Set up Chrome WebDriver (make sure to replace with your ChromeDriver path)
chrome_driver_path = "/Users/sophiacampos/google_reviews/chromedriver"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Function to get restaurant Place IDs in NYC using Google Places API
def get_nyc_restaurants():
    restaurants = []
    places_result = gmaps.places_nearby(location='40.730543, -73.996',  # Stern coordinates
                                        radius=2000,  # 2 km radius
                                        type='restaurant')  # Search for restaurants

    # Loop through the results and extract the place_id
    for place in places_result['results']:
        restaurants.append({
            'Name': place['name'],
            'Place ID': place['place_id']
        })

    # Save the place IDs to a CSV file for reference
    with open('nyc_restaurants.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Name', 'Place ID'])
        writer.writeheader()
        writer.writerows(restaurants)

    print(f"Found {len(restaurants)} restaurants in NYC and saved to 'nyc_restaurants.csv'")
    return [restaurant['Place ID'] for restaurant in restaurants]  # Return only Place IDs

# Function to scrape reviews for a given Google Maps Place ID
def scrape_google_reviews(place_id):
    url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
    driver.get(url)

    time.sleep(3)  # Wait for page to load

    reviews = []
    
    # Find and click on the "See all reviews" button
    try:
        see_all_reviews_button = driver.find_element(By.CSS_SELECTOR, 'button[jsaction="pane.review"]')
        see_all_reviews_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error clicking 'See all reviews' button: {e}")
        return []

    # Scroll through reviews until no new ones are loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop if no new reviews are loaded
        last_height = new_height

    # Scrape reviews using the correct class name
    try:
        review_elements = driver.find_elements(By.CLASS_NAME, 'review-snippet')  # Updated class for review text
        rating_elements = driver.find_elements(By.CLASS_NAME, 'ODSEW-ShBeI-H1e3jb')  # Verify the class name for rating

        for review, rating in zip(review_elements, rating_elements):
            review_text = review.text
            star_rating = rating.get_attribute('aria-label')
            stars = star_rating.split()[0]  # Get the number of stars
            reviews.append({'Review': review_text, 'Rating': stars})

    except Exception as e:
        print(f"Error scraping reviews: {e}")

    return reviews

# Step 1: Fetch NYC restaurant Place IDs using the Google Places API
place_ids = get_nyc_restaurants()

# Step 2: Scrape reviews for each restaurant using Selenium
all_reviews = []
for place_id in place_ids:
    print(f"Scraping reviews for Place ID: {place_id}")
    reviews = scrape_google_reviews(place_id)
    all_reviews.extend(reviews)

# Step 3: Save the scraped reviews to a CSV file
with open('scraped_nyc_google_reviews.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Review', 'Rating'])
    writer.writeheader()
    writer.writerows(all_reviews)

print("Scraping complete. Reviews saved to 'scraped_nyc_google_reviews.csv'")
driver.quit()
