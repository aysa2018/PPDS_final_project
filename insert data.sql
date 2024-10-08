INSERT INTO Users (Username, Email, PasswordHash, Preferences)
VALUES 
('alice_wonder', 'alice@example.com', 'hashed_password_1', '{"cuisine": "Italian", "priceRange": "$$"}'),
('bob_builder', 'bob@example.com', 'hashed_password_2', '{"cuisine": "Mexican", "ambiance": "casual"}'),
('carol_singer', 'carol@example.com', 'hashed_password_3', '{"cuisine": "Sushi", "ratingPreference": "4+"}'),
('dave_gamer', 'dave@example.com', 'hashed_password_4', '{"cuisine": "Chinese", "favoriteDish": "Noodles"}'),
('eve_writer', 'eve@example.com', 'hashed_password_5', '{"cuisine": "Mediterranean", "diet": "Vegetarian"}');

SELECT * FROM Users;

INSERT INTO Restaurants (Name, Address, Latitude, Longitude, CuisineType, PriceRange, Ambiance, Rating, GoogleMapsURL)
VALUES 
('LOS TACOS No.1', '75 9th Ave, New York, NY 10011, USA', 40.742476, -74.006703, 'Mexican', '$$', 'Casual', 4.8, 'https://maps.google.com/?q=LOS+TACOS+No.1'),
('Great Jones Distilling Co', '686 Broadway, New York, NY 10012, USA', 40.727333, -73.992758, 'American', '$$$', 'Trendy', 4.6, 'https://maps.google.com/?q=Great+Jones+Distilling+Co'),
('Piccola Cucina Osteria Siciliana', '190 A St, New York, NY 10012, USA', 40.728666, -73.999864, 'Italian', '$$$', 'Intimate', 4.6, 'https://maps.google.com/?q=Piccola+Cucina+Osteria+Siciliana'),
('Essex', '120 Essex St, New York, NY 10002, USA', 40.720319, -73.981148, 'American', '$$', 'Lively', 4.8, 'https://maps.google.com/?q=Essex'),
('Fish Cheeks', '55 E 1st St, New York, NY 10003, USA', 40.725505, -73.993788, 'Thai', '$$', 'Casual', 4.8, 'https://maps.google.com/?q=Fish+Cheeks'),
('Bar Primi Bowery', '325 Bowery, New York, NY 10003, USA', 40.724600, -73.994857, 'Italian', '$$', 'Casual', 4.4, 'https://maps.google.com/?q=Bar+Primi+Bowery'),
('Gemma', '335 Bowery, New York, NY 10003, USA', 40.724732, -73.996174, 'Italian', '$$', 'Casual', 4.5, 'https://maps.google.com/?q=Gemma');

SELECT * FROM Restaurants;

INSERT INTO Reviews (RestaurantID, UserID, Rating, Comment, ReviewDate) 
VALUES 
(1, 1, 5.0, 'Absolutely loved the tacos! Best in the city.', '2024-10-01 12:30:00'),
(2, 2, 4.5, 'Great cocktails and atmosphere.', '2024-10-02 14:00:00'),
(3, 3, 4.8, 'The pasta was incredible, will definitely return!', '2024-10-03 18:15:00'),
(4, 4, 4.0, 'Good food, but a bit crowded.', '2024-10-04 20:00:00'),
(5, 5, 4.7, 'Delicious and fresh, highly recommend!', '2024-10-05 19:45:00'),
(6, 1, 4.2, 'Nice place for a casual dinner.', '2024-10-06 16:30:00'),
(7, 3, 5.0, 'Gemma is fantastic! Great vibe and even better food.', '2024-10-07 15:00:00');

SELECT * FROM Reviews;

