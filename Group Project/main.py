import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_google_reviews(url):
    reviews = []
    page = 1

    while True:
        response = requests.get(url, params={'start': (page - 1) * 10})
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching page {page}: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract restaurant name
        restaurant_name = soup.find('div', class_='restaurant-name')
        if restaurant_name:
            restaurant_name = restaurant_name.text.strip()
        else:
            restaurant_name = "Unknown Restaurant"

        # Extract review elements
        review_elements = soup.find_all('div', class_='review')
        if not review_elements:
            print(f"No reviews found on page {page}. Stopping.")
            break

        for review_element in review_elements:
            rating = review_element.find('span', class_='star-rating')
            if rating:
                rating = rating.text.strip()
            review = review_element.find('p', class_='review-text')
            if review:
                review = review.text.strip()

            # Append review details to the list
            reviews.append({
                'restaurant_name': restaurant_name,
                'rating': rating if rating else 'N/A',
                'text': review if review else 'N/A'
            })

        # Find the "Next" button for pagination
        next_page_button = soup.find('a', id='pnnext')
        if not next_page_button:
            print("No more pages.")
            break

        # Handle relative URLs for next page
        next_page_url = next_page_button['href']
        url = f"https://www.google.com{next_page_url}"

        # Implement rate limiting to avoid overloading the server
        time.sleep(2)
        page += 1

    return reviews

def save_to_csv(reviews, filename):
    # Save scraped reviews to CSV
    if not reviews:
        print("No reviews to save.")
        return

    keys = reviews[0].keys()  # Use keys from the first review as CSV headers
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()  # Write the CSV header
        dict_writer.writerows(reviews)  # Write all reviews to the CSV file

# Example usage
restaurant_url = "https://www.google.com/search?q=restaurants+near+new+york+ny..."
all_reviews = scrape_google_reviews(restaurant_url)

if all_reviews:
    save_to_csv(all_reviews, 'restaurant_reviews.csv')
    print("Reviews saved successfully!")
else:
    print("No reviews to save.")