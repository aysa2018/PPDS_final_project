CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    Preferences JSON
);

CREATE TABLE Restaurants (
    RestaurantID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Latitude DECIMAL(9,6) NOT NULL,
    Longitude DECIMAL(9,6) NOT NULL,
    CuisineType VARCHAR(100),
    PriceRange VARCHAR(50),
    Ambiance VARCHAR(100),
    Rating DECIMAL(2,1) CHECK (Rating BETWEEN 0 AND 5),
    GoogleMapsURL VARCHAR(255)
);

CREATE TABLE Reviews (
    ReviewID SERIAL PRIMARY KEY,
    RestaurantID BIGINT UNSIGNED,
    UserID BIGINT UNSIGNED,
    Rating DECIMAL(2,1) CHECK (Rating BETWEEN 0 AND 5),
    Comment TEXT,
    ReviewDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Discounts (
    DiscountID INT AUTO_INCREMENT PRIMARY KEY,
    RestaurantID BIGINT UNSIGNED,    
    DiscountDescription VARCHAR(255),
    DiscountAmount DECIMAL(5, 2),     
    ValidDays VARCHAR(100),          
    StartDate DATE,                  
    EndDate DATE,                    
    FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID)
);

CREATE TABLE SearchQueries (
    QueryID INT AUTO_INCREMENT PRIMARY KEY,
    UserID BIGINT UNSIGNED,           
    MoodID INT,                      
    SentimentKeywords VARCHAR(255),
    FilterCriteria JSON,
    SearchDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MoodID) REFERENCES Moods(MoodID)
);

CREATE TABLE Moods (
    MoodID INT AUTO_INCREMENT PRIMARY KEY,
    MoodName VARCHAR(100) NOT NULL,
    Description TEXT
);
 
