-- Table to store user information such as username, email, password, and preferences
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,                -- Unique identifier for each user
    Username VARCHAR(50) NOT NULL UNIQUE,     -- Username, must be unique and not null
    Email VARCHAR(100) NOT NULL UNIQUE,       -- User email, must be unique and not null
    PasswordHash VARCHAR(255) NOT NULL,       -- Hashed password for security
    Preferences JSON                          -- JSON field to store user preferences, such as favorite cuisines
);

-- Table to store restaurant information such as name, location, and ratings
CREATE TABLE Restaurants (
    RestaurantID SERIAL PRIMARY KEY,          -- Unique identifier for each restaurant
    Name VARCHAR(100) NOT NULL,               -- Restaurant name, must be provided
    Address VARCHAR(255) NOT NULL,            -- Restaurant address, must be provided
    Latitude DECIMAL(9,6) NOT NULL,           -- Latitude for restaurant's geolocation, precise to 6 decimal places
    Longitude DECIMAL(9,6) NOT NULL,          -- Longitude for restaurant's geolocation, precise to 6 decimal places
    CuisineType VARCHAR(100),                 -- Type of cuisine offered (e.g., Italian, Japanese)
    PriceRange VARCHAR(50),                   -- Price range category (e.g., $, $$, $$$)
    Ambiance VARCHAR(100),                    -- Describes the ambiance (e.g., cozy, formal)
    Rating DECIMAL(2,1) CHECK (Rating BETWEEN 0 AND 5), -- Average rating, must be between 0 and 5
    GoogleMapsURL VARCHAR(255)                -- URL to the restaurant's location on Google Maps
);

-- Table to store reviews by users for restaurants
CREATE TABLE Reviews (
    ReviewID SERIAL PRIMARY KEY,              -- Unique identifier for each review
    RestaurantID BIGINT UNSIGNED,             -- Reference to the reviewed restaurant
    UserID BIGINT UNSIGNED,                   -- Reference to the user who posted the review
    Rating DECIMAL(2,1) CHECK (Rating BETWEEN 0 AND 5), -- Review rating, must be between 0 and 5
    Comment TEXT,                             -- Text of the user's review
    ReviewDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically sets the review date to the current timestamp
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID), -- Foreign key referencing the Restaurants table
    FOREIGN KEY (UserID) REFERENCES Users(UserID) -- Foreign key referencing the Users table
);

-- Table to store discount information for restaurants
CREATE TABLE Discounts (
    DiscountID INT AUTO_INCREMENT PRIMARY KEY, -- Unique identifier for each discount
    RestaurantID BIGINT UNSIGNED,              -- Reference to the restaurant offering the discount
    DiscountDescription VARCHAR(255),          -- Description of the discount (e.g., 20% off)
    DiscountAmount DECIMAL(5, 2),              -- The amount of the discount in decimal format
    ValidDays VARCHAR(100),                    -- Days the discount is valid (e.g., 'Mon-Fri')
    StartDate DATE,                            -- Start date of the discount
    EndDate DATE,                              -- End date of the discount
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) -- Foreign key referencing the Restaurants table
);

-- Table to store user search queries related to restaurant suggestions based on mood and filters
CREATE TABLE SearchQueries (
    QueryID INT AUTO_INCREMENT PRIMARY KEY,    -- Unique identifier for each search query
    UserID BIGINT UNSIGNED,                    -- Reference to the user making the query
    MoodName VARCHAR(255),                     -- Stores the mood related to the query
    SentimentKeywords VARCHAR(255),            -- Extracted keywords based on user's sentiment or mood
    FilterCriteria JSON,                       -- JSON object storing any additional filters applied (e.g., price range)
    SearchDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically sets the search date to the current timestamp
    FOREIGN KEY (UserID) REFERENCES Users(UserID),  -- Foreign key referencing the Users table
    FOREIGN KEY (MoodID) REFERENCES Moods(MoodID)   -- Foreign key referencing the Moods table
);

-- Table to store different moods related to restaurants
CREATE TABLE UserMood (                        
    UserID BIGINT UNSIGNED NOT NULL,           -- Reference to the user making the query
    MoodName VARCHAR(255) NOT NULL,            -- Identified moods of the user
    FOREIGN KEY (UserID) REFERENCES Users(UserID)  -- Foreign key referencing the Users Table
);


-- Table to store different moods related to restaurants
CREATE TABLE RestaurantMood (
    RestaurantID BIGINT UNSIGNED NOT NULL,    -- Reference to the Restaurant 
    MoodName VARCHAR(255) NOT NULL,           -- Identified moods of the Restaurants
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID) -- Foreign key referencing the Restaurants Table
);
