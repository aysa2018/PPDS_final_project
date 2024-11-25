## BistroMoods

BistroMoods is a web application that helps users find restaurants based on their moods. The data model captures essential information about users, moods, restaurants, reviews, ect. It connects users' emotional states with restaurant recommendations through a relational database, enabling the application to analyze reviews and suggest dining options that align with users' feelings.

## Features
- **Mood-Based Recommendations**: Enter a mood, and BistroMoods finds matching restaurants.
- **Dynamic Restaurant Listings**: Displays restaurant details in an interactive card layout.
- **Interactive UI**: Cards with hover effects and clickable links redirect to Yelp.
- **Custom Filters**: Supports filters like rating, price range, dietary restrictions, and special features.

---

## Repository Structure

### Backend: **[bistromoods](https://github.com/yourusername/bistromoods)**


### Frontend: **[bistromoods_frontend](https://github.com/yourusername/bistromoods_frontend)**




## Link to ER Diagram 
https://lucid.app/lucidchart/65c785fc-db1b-4660-861f-f5b31761855a/edit?viewport_loc=-1978%2C-1597%2C2327%2C1383%2C0_0&invitationId=inv_7a023b2d-4867-4d8b-9e50-30a211190691



## Installation

### 1. Clone the Repository

- Clone this repository or download the source code:
  ```bash
  git clone https://github.com/aysa2018/bistromoods.git
  cd bistromoods
  ```

### 2. FastAPI Server Setup

After setting up the database, follow these steps to install and run the FastAPI server.

  1. Create and activate a virtual enviornment:
     
  - Create a virtual environment:
   
  ```bash
  python -m venv .venv
  ```
  or 

  ```bash
  python3 -m venv .venv
  ```

  - Activate the virtual enviornment
  For Linux/macOS
  ```
  .venv\Scripts\activate
  ```

  For Windows
  ```
  venv\Scripts\activate
  ```
  2. Install required packages:
     
  ```bash
  pip install -r requirements.txt
  ```
  or 

  ```bash
  pip3 install -r requirements.txt
  ```

  3. Run the backend server:
  ```bash
  uvicorn main:app --reload
  ```
### 3. Frontend
- Clone this repository or download the source code for frontend:
  ```bash
  git clone https://github.com/aysa2018/bistromoods_frontend.git
  cd bistromoods_frontend
  ```

- Install dependencies:
  ```bash
    npm install
  ```
- Start the frontend server:
  ```bash
    npm start
  ```
- Access the application: 
  
  Open your browser and navigate to http://localhost:3000

Once both repositories are cloned, for further use, just run the backend server and frontend server at the same time with
  ```bash
  uvicorn main:app --reload
  ```
  for backend 
  and 

  ```bash
    npm start
  ```
  for frontend.

## Usage
1. Open the frontend in your browser.
2. Enter a mood (e.g., "happy") in the search box.
3. View recommended restaurants displayed in an interactive card layout.
4. Click on a restaurant card to open its Yelp page for more details.

## Technical Details

### Backend
- **Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Natural Language Processing**: spaCy for keyword extraction
- **Dependencies**:
  - FastAPI
  - SQLAlchemy
  - Passlib (for authentication)

### Frontend
- **Framework**: React
- **Styling**: CSS modules
- **APIs Used**:
  - Custom FastAPI endpoints
  - Yelp API (optional, for additional details)
  - OpenAI API

## Libraries Used

The BistroMoods backend utilizes several key libraries:

- **FastAPI**: Provides the framework to build and manage all API endpoints.
- **SQLAlchemy**: Handles interactions with the MySQL database, including table creation and queries.
- **pymysql**: Database Driver
- **Pydantic**: Ensures validation and proper formatting of API requests and responses.
- **Uvicorn**: Runs the FastAPI application, providing a fast and reliable server.
- **fuzzywuzzy**: Library for keyword matching and text similarity.
- **passlib[bcrypt]**: Provides password hashing for secure user authentication.

These libraries ensure the backend efficiently manages data while enabling users to access and interact with restaurant recommendations seamlessly.




## License
This project is licensed under the MIT License. 

---
