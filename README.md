# Cast Quest 

Cast Quest is a movie-actor connection game that challenges players to find the shortest path between two actors through their shared movie appearances.  

## Overview  

This project implements concepts such as **graph traversal**, **BFS (Breadth-First Search)**, and **session management** using Flask. Players start with an initial actor and attempt to reach a target actor by selecting co-stars from movies they’ve worked in.  

## Features  

- **Find the Shortest Path**: Uses BFS to determine the least degrees of separation between two actors.  
- **Interactive Gameplay**: Users progressively reveal connections between actors through movie collaborations.  
- **Error Handling**: Players have limited attempts before being reset to their last correct selection.  
- **Session Storage**: Game state is preserved between interactions using Flask sessions.  

## Algorithm  

The core functionality is built on **BFS**, ensuring the shortest possible connection path is found:  

1. **Load the Dataset**: Actor and movie information is imported from CSV files.  
2. **Graph Representation**: Actors and movies form a bidirectional graph where edges represent shared movie appearances.  
3. **Pathfinding with BFS**: The algorithm searches for the shortest path between the source and target actors.  
4. **User Interaction**: The game provides feedback and updates session state dynamically.  

## Example  

If **Dwayne Johnson** is the starting actor and **Tom Cruise** is the target, BFS finds a path like:  

1. *Dwayne Johnson* → starred in *Movie A* with *Actor X*  
2. *Actor X* → starred in *Movie B* with *Tom Cruise*  

This results in **2 degrees of separation**.  

## Installation & Setup  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/cast-quest.git
   cd cast-quest
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the application:
   ```bash
   python app.py
4. Run the application:
   ```bash
   http://127.0.0.1:5000

## Technologies Used 

- **Python, Flask**: Backend framework and web server
- **HTML, CSS, JavaScript**: Frontend for user interaction
- **CSV Data Processing**: Loads movie-actor relationships

