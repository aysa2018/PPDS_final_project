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
1. Use the `git clone` command to clone the repository to download the database to your local machine.
2. Open MySQL Workbench and create a new database on your local machine, then select it.
3. Load and execute the SQL script by going to File > Open SQL Script. Navigate to the cloned repository folder where the SQL script is located. Select the SQL script file and open it.
4. Once the script is loaded into the editor, click the Execute button (the lightning bolt icon) to run the script. This will create the tables in the selected database.

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


