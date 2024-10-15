## BistroMoods

BistroMoods is a web application that helps users find restaurants based on their moods. The data model captures essential information about users, moods, restaurants, reviews, ect. It connects users' emotional states with restaurant recommendations through a relational database, enabling the application to analyze reviews and suggest dining options that align with users' feelings.

## Data Model

The BistroMoods data model is designed to connect user moods with restaurant recommendations. It consists of six main entities:

- **Users:** Stores user information, including usernames and emails, along with preferences for cuisine and dietary restrictions.
- **Moods:** Represents different emotional states influencing restaurant choices, such as “Happy,” “Relaxed,” or “Adventurous.” This enhances the search functionality by allowing users to filter based on their current feelings.
- **Restaurants:** Contains details about various restaurants, including names, addresses, cuisine types, price ranges, ambiance, and average ratings.
- **Discounts:** Stores information about discounts offered by restaurants, allowing users to find cost-effective dining options.
- **Reviews:** Links users to their feedback on restaurants, capturing ratings and comments, which are essential for personalized recommendations.
- **SearchQueries:** Tracks user search queries to analyze preferences and improve recommendations based on user moods.

These entities interact to enable users to find restaurants that match their moods based on the analysis of reviews and available discounts.

## Why SQL?
We chose SQL for BistroMoods due to its structured nature, which is well-suited for managing the relationships between moods, users, restaurants, and reviews. SQL databases allow for efficient querying and retrieval of data, crucial for providing personalized restaurant recommendations based on user mood. Additionally, SQL helps ensure data integrity and consistency through enforced relationships and constraints, making it an ideal choice for this project.

## Prerequisites
- MySQL Server
- MySQL Workbench 
  
## Setup
1. Use the `git clone` command to clone the repository to download the SQL script to your local machine.
2. Open MySQL Workbench and create a new database on your local machine, then select it.
3. Load and execute the SQL script by going to File > Open SQL Script. Navigate to the cloned repository folder where the SQL script is located. Select the SQL script file: bistromoods.sql and open it.
4. Once the script is loaded into the editor, click the Execute button (the lightning bolt icon) to run the script. This will create the tables in the selected database.
5. After creating the tables ensure to also open and excecute the insertdata.sql to load the freshly created tables with representative data.
6. Once the insertdata.sql script is excecuted the data table is ready for use.

## Usage
In the BistroMoods web application, users will interact with a user-friendly front end, while the back end will handle all interactions with the database. Here’s how the database will be utilized:

1. **User Registration and Management:** 
   - Users will register through the front end, providing their usernames, emails, and password. This information will be securely stored in the **Users** table by the back end.
  
2. **Mood Selection:**
   - When users select their current mood on the front end, the application will use the back end to query the **Moods** table. This selection will influence the restaurant recommendations.

3. **Restaurant Recommendations:**
   - Users can input their mood and any additional preferences through the front end. The back end will query the **Restaurants** table based on this input, considering filters like cuisine type or price range.
   - The response will include restaurant details such as name, address, ambiance, rating, and any active discounts from the **Discounts** table.

4. **Search Queries Tracking:**
   - Each search made by users will be logged in the **SearchQueries** table by the back end, capturing the mood, sentiment keywords, and any filters used. This will assist in refining the recommendation algorithm based on user preferences over time.

By implementing this architecture, the database will facilitate seamless interactions between the front end and back end, ensuring personalized and relevant dining options based on users' moods without direct database access.

## Link to ER Diagram 
https://lucid.app/lucidchart/65c785fc-db1b-4660-861f-f5b31761855a/edit?viewport_loc=-1978%2C-1597%2C2327%2C1383%2C0_0&invitationId=inv_7a023b2d-4867-4d8b-9e50-30a211190691

## API Endpoints

We used **FastAPI** and **MySQL** to create an API for managing restaurant recommendations based on user moods. This API allows you to create, view, update, and delete **users**, **restaurants**, **reviews**, and **mood-related** data.

## Setting Up & Running Instructions

### 1. Setting up Database
- Clone this repository or download the source code:
  ```bash
  git clone https://github.com/aysa2018/PPDS_final_project.git
  cd PPDS_final_project
  ```

- Create a virtual environment:
  ```bash
  python -m venv .venv
  ```


- Install the required packages:
  ```bash
  pip install -r requirements.txt
  ```

- Create a `.env` file in the project root directory with your database connection string:
  ```
  DATABASE_URL='mysql+pymysql://username:password@host:port/database_name'
  ```
  Replace `username`, `password`, `host`, `port`, and `database_name` with your actual MySQL database credentials.

### 2. Running the API
- Run the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```

- The API docs for testing are available at:
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or [http://localhost:8000/docs](http://localhost:8000/docs).

### 3. Using Postman to Interact with the API
You can use our API in your Postman. Here are examples of a few endpoints:

**1. Get All Users**
- GET `/users/`

**2. Create a New User**
- POST `/users/`
  - Example Request Body:
  ```json
  {
    "Username": "alice",
    "Email": "alice@example.com",
    "Password": "password123",
    "Preferences": {
      "Cuisine": "Italian"
    }
  }
  ```

**3. Create a New Review**
- POST `/reviews/`
  - Example Request Body:
  ```json
  {
    "RestaurantID": 1,
    "UserID": 1,
    "Rating": 4.5,
    "Comment": "Amazing food!"
  }
  ```


## Usage
To run the application:
```bash
python main.py
```
Follow the on-screen instructions to interact with the API and manage users, restaurants, and reviews.

## Libraries Used

The BistroMoods backend utilizes several key libraries:

- **FastAPI**: Provides the framework to build and manage all API endpoints.
- **SQLAlchemy**: Handles interactions with the MySQL database, including table creation and queries.
- **Pydantic**: Ensures validation and proper formatting of API requests and responses.
- **Uvicorn**: Runs the FastAPI application, providing a fast and reliable server.

These libraries ensure the backend efficiently manages data while enabling users to access and interact with restaurant recommendations seamlessly.
