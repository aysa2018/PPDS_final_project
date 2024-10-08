## BistroMoods

BistroMoods is a web application that helps users find restaurants based on their moods. The data model captures essential information about users, moods, restaurants, and reviews. It connects users' emotional states with restaurant recommendations through a relational database, enabling the application to analyze reviews and suggest dining options that align with users' feelings.

## Data Model

The BistroMoods data model is designed to connect user moods with restaurant recommendations. It consists of four main entities:

- Users: Stores user information including usernames and emails.
- Moods: Represents different emotional states that influence restaurant choices.
- Restaurants: Contains details about various restaurants, including their names and locations.
- Reviews: Links users to their feedback on restaurants, capturing ratings and comments.

These entities interact to enable users to find restaurants that match their moods based on the analysis of reviews.

## Why SQL?
We chose SQL for BistroMoods due to its structured nature, which perfectly suited for managing the relationships between moods, users, restaurants, and reviews. Furthermore, since SQL databases allow for efficient querying and retrieval of data, which will be crucial for providing personalized restaurant recommendations based on user mood, SQL became an even more enticing choice. Additionally, the use of SQL will help to ensure data integrity and consistency through enforced relationships and constraints, making it an ideal choice for this project.

## Prerequisites
- MySQL Server
- MySQL Workbench 
  
## Setup & Usage
1. Use the git clone command to clone the repository to download the database to your local machine.
2. Open the MySQL Workbench and create a new database on your local machine and select it.
3. Load and Execute the SQL Script by going to File > Open SQL Script. Navigate to the cloned repository folder where the SQL script is located. Select the SQL script file and open it.
4. Once the script is loaded into the editor, click the Execute button (the lightning bolt icon) to run the script. This will create the tables in the selected database.

## Link to ER Diagram 
https://lucid.app/lucidchart/65c785fc-db1b-4660-861f-f5b31761855a/edit?viewport_loc=-1978%2C-1597%2C2327%2C1383%2C0_0&invitationId=inv_7a023b2d-4867-4d8b-9e50-30a211190691


