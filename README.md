# OMDB
Fetched 100 movies from OMDB API.    
- Movies are saved in the database.   
- This method runs only once if database is empty.
- This method is automated.    
## 2. Implemented an api class in the api folder for the data class  - The api has a method that returns the list of movies from the database   - There is an option to set how many records are returned in single API response (by default 10)   - There's pagination implemented in the backend   - Data is ordered by Title - The api has a method that returns single movie from the database   - There is an option to get the movie by title - The api has a method to add movie to the database   - Title is provided in request   - All movie details are fetched from OMDB API and saved in the database - The api has a method to remove a movie from the database   - There is an option to remove movie with it's id   - This method is protected and only authorized user can perform this action (There is test user in the database)
