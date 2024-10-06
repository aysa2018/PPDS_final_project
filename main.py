import time
import csv  # Import CSV module
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(), options=chrome_options)

# Open the Google Maps page for restaurants in NYC
url = "https://www.google.com/maps/search/restaurants+near+NYC,+NY/@40.7262374,-73.9974596,15z?entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scrape restaurant names and ratings
restaurants = []
restaurant_elements = driver.find_elements(By.CSS_SELECTOR, 'div.bfdHYd.Ppzolf.OFBs3e')

for restaurant in restaurant_elements:
    try:
        # Get restaurant name from <div class="qBF1Pd">
        name_element = restaurant.find_element(By.CSS_SELECTOR, 'div.qBF1Pd')
        name = name_element.text if name_element else "No name"

        # Get restaurant rating and remove the "number of reviews"
        rating_element = restaurant.find_element(By.CSS_SELECTOR, 'span[aria-label*="stars"]')
        rating_text = rating_element.get_attribute("aria-label") if rating_element else "No rating"
        
        # Extract only the star rating number (e.g., "4.5 stars" -> "4.5")
        rating = rating_text.split(" ")[0] if rating_text else "No rating"

        # Append to the restaurants list
        restaurants.append((name, rating))
        
    except Exception as e:
        print(f"Error extracting data: {e}")

# Close the WebDriver
driver.quit()

# Write the data to a CSV file
csv_restaurantdata = 'restaurants_nyc.csv'
with open(csv_restaurantdata, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Restaurant Name', 'Rating'])  # Write header
    writer.writerows(restaurants)  # Write restaurant data

print(f"Data has been written to {csv_restaurantdata}")