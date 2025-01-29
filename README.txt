Cast Quest

This project incorporates various concepts from 112 including an advanced form of backtracking and recursion. The essence of this project is a game where we start with an initial movie actor and target movie actor. 

A breadth first search algorithm determines the path with the least degrees of separation between the actors. For example, choosing “Dwyane Johnson” as the source name and “Tom Cruise” as the target, will result in two degrees of separation, where Tom Cruise and Dwayne Johnson both acted with actors in different movies. 3 degrees of separation means Tom Cruise is acted in a movie with another actor who acted in a different movie with another actor who acted with Dwyane Johnson. 

A more nuanced approach to a backtracking algorithm, Breadth First Search, our algorithm gives the shortest path between the source and target actors. 

Our game allows users to try to achieve this shortest path in a fun manner. Whenever the user detracts from the optimal path from more than 3 errors away, we give a personalized hint to the user to get them on path. 

Modules Needed to be downloaded
- CSV
- Temp (for TempFile)
- Flask
- HTML, CSS, JS
- Run app.py


