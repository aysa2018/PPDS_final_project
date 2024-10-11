-- Inserting sample user data with username, email, password hash, and preferences stored in JSON format
INSERT INTO Users (Username, Email, PasswordHash, Preferences)
VALUES 
('alice_wonder', 'alice@example.com', 'hashed_password_1', '{"cuisine": "Italian", "priceRange": "$$"}'), -- Alice prefers Italian food with a moderate price range
('bob_builder', 'bob@example.com', 'hashed_password_2', '{"cuisine": "Mexican", "ambiance": "casual"}'), -- Bob enjoys casual Mexican dining
('carol_singer', 'carol@example.com', 'hashed_password_3', '{"cuisine": "Sushi", "ratingPreference": "4+"}'), -- Carol prefers sushi restaurants with a rating of 4 or higher
('dave_gamer', 'dave@example.com', 'hashed_password_4', '{"cuisine": "Chinese", "favoriteDish": "Noodles"}'), -- Dave is a fan of Chinese cuisine, especially noodles
('eve_writer', 'eve@example.com', 'hashed_password_5', '{"cuisine": "Mediterranean", "diet": "Vegetarian"}'); -- Eve enjoys Mediterranean food with a vegetarian diet

-- Selecting all users to verify insertions
SELECT * FROM Users;

-- Inserting restaurant data including name, address, geolocation, cuisine type, price range, ambiance, rating, and Google Maps URL
INSERT INTO Restaurants (Name, Address, Latitude, Longitude, CuisineType, PriceRange, Ambiance, Rating, GoogleMapsURL)
VALUES 
('LOS TACOS No.1', '75 9th Ave, New York, NY 10011, USA', 40.742476, -74.006703, 'Mexican', '$$', 'Casual', 4.8, 'https://maps.google.com/?q=LOS+TACOS+No.1'), -- Popular casual Mexican restaurant
('Great Jones Distilling Co', '686 Broadway, New York, NY 10012, USA', 40.727333, -73.992758, 'American', '$$$', 'Trendy', 4.6, 'https://maps.google.com/?q=Great+Jones+Distilling+Co'), -- Trendy American restaurant with a high-end feel
('Piccola Cucina Osteria Siciliana', '190 A St, New York, NY 10012, USA', 40.728666, -73.999864, 'Italian', '$$$', 'Intimate', 4.6, 'https://maps.google.com/?q=Piccola+Cucina+Osteria+Siciliana'), -- Intimate Sicilian Italian restaurant
('Essex', '120 Essex St, New York, NY 10002, USA', 40.720319, -73.981148, 'American', '$$', 'Lively', 4.8, 'https://maps.google.com/?q=Essex'), -- Lively American restaurant
('Fish Cheeks', '55 E 1st St, New York, NY 10003, USA', 40.725505, -73.993788, 'Thai', '$$', 'Casual', 4.8, 'https://maps.google.com/?q=Fish+Cheeks'), -- Casual Thai restaurant
('Bar Primi Bowery', '325 Bowery, New York, NY 10003, USA', 40.724600, -73.994857, 'Italian', '$$', 'Casual', 4.4, 'https://maps.google.com/?q=Bar+Primi+Bowery'), -- Casual Italian restaurant
('Gemma', '335 Bowery, New York, NY 10003, USA', 40.724732, -73.996174, 'Italian', '$$', 'Casual', 4.5, 'https://maps.google.com/?q=Gemma'); -- Italian restaurant with a casual ambiance

-- Selecting all restaurants to verify insertions
SELECT * FROM Restaurants;

-- Inserting review data, linking users to restaurants with ratings, comments, and timestamps
INSERT INTO Reviews (RestaurantID, UserID, Rating, Comment, ReviewDate) 
VALUES 
(1, 1, 5.0, 'Absolutely loved the tacos! Best in the city.', '2024-10-01 12:30:00'), -- Alice loved the tacos at LOS TACOS No.1
(2, 2, 4.5, 'Great cocktails and atmosphere.', '2024-10-02 14:00:00'), -- Bob enjoyed the cocktails and vibe at Great Jones Distilling Co
(3, 3, 4.8, 'The pasta was incredible, will definitely return!', '2024-10-03 18:15:00'), -- Carol had an amazing experience at Piccola Cucina
(4, 4, 4.0, 'Good food, but a bit crowded.', '2024-10-04 20:00:00'), -- Dave found Essex a bit crowded but liked the food
(5, 5, 4.7, 'Delicious and fresh, highly recommend!', '2024-10-05 19:45:00'), -- Eve enjoyed a fresh meal at Fish Cheeks
(6, 1, 4.2, 'Nice place for a casual dinner.', '2024-10-06 16:30:00'), -- Alice returned to review Bar Primi
(7, 3, 5.0, 'Gemma is fantastic! Great vibe and even better food.', '2024-10-07 15:00:00'); -- Carol loved her meal at Gemma

-- Selecting all reviews to verify insertions
SELECT * FROM Reviews;


-- Inserting sample moods for users
INSERT INTO UserMood (UserID, MoodName)
VALUES 
(1, 'Happy'),      -- Alice is feeling happy
(2, 'Excited'),    -- Bob is feeling excited
(3, 'Relaxed'),    -- Carol is feeling relaxed
(4, 'Hungry'),     -- Dave is feeling hungry
(5, 'Adventurous'); -- Eve is feeling adventurous

SELECT * FROM UserMood;


-- Inserting sample moods for restaurants
INSERT INTO RestaurantMood (RestaurantID, MoodName)
VALUES 
(1, 'Casual'),         -- LOS TACOS No.1 has a casual mood
(2, 'Trendy'),         -- Great Jones Distilling Co has a trendy mood
(3, 'Intimate'),       -- Piccola Cucina Osteria Siciliana has an intimate mood
(4, 'Lively'),         -- Essex has a lively mood
(5, 'Casual'),         -- Fish Cheeks has a casual mood
(6, 'Casual'),         -- Bar Primi Bowery has a casual mood
(7, 'Casual');         -- Gemma has a casual mood

SELECT * FROM RestaurantMood;

-- Inserting data into the updated SearchQueries table
INSERT INTO SearchQueries (UserID, MoodName, SentimentKeywords, FilterCriteria, SearchDate)
VALUES
(1, 'Happy', 'Happy', '{}', '2024-10-06 16:40:00'),     -- Alice searched for a happy mood experience
(2, 'Excited', 'Music', '{}', '2024-10-04 10:05:00'),   -- Bob searched with a "music" keyword while being excited
(3, 'Relaxed', 'Chill', '{}', '2024-10-05 09:09:09'),   -- Carol was in a relaxed mood, searching for something chill
(4, 'Hungry', 'Love', '{}', '2024-10-07 20:00:00'),     -- Dave searched with a romantic "love" mood while feeling hungry
(3, 'Adventurous', 'Classy', '{}', '2024-10-07 10:00:00'); -- Carol was looking for a classy dining experience while feeling adventurous

-- Selecting all search queries to verify insertions
SELECT * FROM SearchQueries;

-- Inserting discount information for different restaurants
INSERT INTO Discounts (RestaurantID, DiscountDescription, DiscountAmount, ValidDays, StartDate, EndDate)
VALUES
(1, '10% off for first-time customers', 10.00, 'Mon,Tue,Wed', '2024-10-01', '2024-12-31'), -- Discount for first-time customers at LOS TACOS No.1
(2, 'Buy 1 Get 1 Free', 50.00, 'Thu,Fri', '2024-11-01', '2024-11-30'), -- BOGO deal at Great Jones Distilling Co
(3, '20% off all orders over $50', 20.00, 'Sat,Sun', '2024-12-01', '2024-12-31'), -- Discount on large orders at Piccola Cucina
(4, 'Free dessert with any meal', 0.00, 'Mon,Thu', '2024-10-15', '2024-11-15'), -- Free dessert deal at Essex
(5, '15% off for students', 15.00, 'Fri,Sat', '2024-09-01', '2024-10-31'); -- Student discount at Fish Cheeks

-- Selecting all discounts to verify insertions
SELECT * FROM Discounts;
