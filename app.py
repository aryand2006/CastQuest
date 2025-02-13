import csv
import sys
import json
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            names.setdefault(row["name"].lower(), set()).add(row["id"])

    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    # elif len(person_ids) > 1:
    #     print(f"Multiple matches for '{name}': {person_ids}")

    #     return None
    
    else:
        return person_ids[0]



def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    """
    from collections import deque

    start = (source, [])
    queue = deque([start])
    explored = set()

    while queue:
        current_person, path = queue.popleft()

        if current_person == target:
            return path

        explored.add(current_person)

        for movie_id, person_id in neighbors_for_person(current_person):
            if person_id not in explored:
                queue.append((person_id, path + [(movie_id, person_id)]))

    return None

def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for star in movies[movie_id]["stars"]:
            neighbors.add((movie_id, star))
    return neighbors

def get_movies_and_actors(name):
    """
    Takes in a person's name and returns all movie names they starred in along with their co-stars.
    """
    person_id = person_id_for_name(name)
    #print(person_id)
    if not person_id:
        return {}

    movie_ids = people[person_id]["movies"]
    #print(movie_ids)
    movies_and_people = {}

    for movie_id in movie_ids:
        movies_and_people[movies[movie_id]["title"]] = [
            people[star]["name"] for star in movies[movie_id]["stars"]
        ]
    #print(movies_and_people)
    return movies_and_people
@app.route("/", methods=["GET", "POST"])
def game():
    if request.method == "POST":
        start_actor = request.form.get("startActor")
        end_actor = request.form.get("endActor")

        if not start_actor or not end_actor:
            return render_template("index.html", error="Both actors are required!")

        source = person_id_for_name(start_actor)
        target = person_id_for_name(end_actor)

        if source is None or target is None:
            error_msg = f"Actor '{start_actor}' not found!" if source is None else f"Actor '{end_actor}' not found!"
            return render_template("index.html", error=error_msg)

        # Initialize session variables
        session["start_actor"] = start_actor
        session["end_actor"] = end_actor
        session["shortest_path_list"] = shortest_path(source, target) or []
        print(session["shortest_path_list"])
        session["displaying_actors"] = [start_actor]
        session["error"] = 0
        session["last_correct_actor"] = start_actor

        return redirect("/repetitive")

    return render_template("index.html")


@app.route("/repetitive", methods=["GET", "POST"])
def repetitive():
    if request.method == "POST":
        data = request.json
        actor_got_clicked = data.get("actorClicked")

        if not actor_got_clicked:
            return jsonify({"error": "Actor name is required."}), 400

        displaying_actors = session.get("displaying_actors", [])
        shortest_path_list = session.get("shortest_path_list", [])
        error = session.get("error", 0)

        displaying_actors.append(actor_got_clicked)
        dict_of_movies_and_actors = get_movies_and_actors(actor_got_clicked)
        print(shortest_path_list)
        new_list = []
        for i in shortest_path_list:
            new_list.append(i[1])
        print(person_id_for_name(actor_got_clicked), i)
        if person_id_for_name(actor_got_clicked) in new_list:
            session["error"] = 0
            session["last_correct_actor"] = actor_got_clicked
            if actor_got_clicked == session["end_actor"]:
                print(f"{len(shortest_path_list)} degrees of separation.")
                s = ""
                s += f"{len(shortest_path_list)} degrees of separation." + "\n"
                start = session["start_actor"]
                print("YAYYYY", people[shortest_path_list[0][1]])
                man_of_the_hour = people[shortest_path_list[0][1]]["name"]
                movie_of_the_hour = movies[shortest_path_list[0][0]]["title"]
                s += f"1. {start}" + f" and {man_of_the_hour} starred together in {movie_of_the_hour}" + "\n"
                for i in range(1, len(shortest_path_list)):
                    person1 = shortest_path_list[i-1][1]
                    person2 = shortest_path_list[i][1]
                    starredMovie = shortest_path_list[i][0]
                    #print(f"{i+1}: {people[person1][0]} and {people[person2][0]} starred in {movies[starredMovie][0]}")
                    man_of_the_hour = people[person1]["name"]
                    man_of_the_hour2 = people[person2]["name"]
                    movie_of_the_hour = movies[starredMovie]["title"]
                    s += f"{i+1}: {man_of_the_hour} and {man_of_the_hour2} starred in {movie_of_the_hour}" + "\n"

                # for i in range(len(shortest_path_list)):
                #     person1 = people[shortest_path_list[i][1]]["name"]
                    
                #     person2 = people[shortest_path_list[i + 1][1]]["name"]
                #     movie = movies[shortest_path_list[i + 1][0]]["title"]
                #     print(f"{i + 1}: {person1} and {person2} starred in {movie}")
                #     s += f"{i + 1}: {person1} and {person2} starred in {movie}" + "\n"
                
                return jsonify({"message": f"Game won! The optimal path was: {s}"})
        else:
            session["error"] += 1
            if session["error"] >= 3:
                session["error"] = 0
                
                print(displaying_actors)
                if "last_correct_actor" not in session:
                    session["last_correct_actor"] = session["start_actor"]
                last_correct_actor = displaying_actors.index(session["last_correct_actor"])
                displaying_actors = displaying_actors[:last_correct_actor+1]
                print("YAY", last_correct_actor, displaying_actors)
                dict_of_movies_and_actors = get_movies_and_actors(session["last_correct_actor"])
                return jsonify({
                    "message": "You made too many mistakes! Returning to the last correct actor.",
                    "lastCorrectActor": last_correct_actor,
                    "moviesAndActors": dict_of_movies_and_actors,
                    "displaying_actors": displaying_actors
                })

        session["displaying_actors"] = displaying_actors
        return jsonify({"message": "On the way!", "moviesAndActors": dict_of_movies_and_actors})

    # Return JSON data if the request explicitly asks for JSON (for fetch requests)
    if request.headers.get("Accept") == "application/json":
        displaying_actors = session.get("displaying_actors", [session.get("start_actor")])
        if not displaying_actors:
            return jsonify({"error": "No actor data available."}), 400

        last_actor = displaying_actors[-1]
        dict_of_movies_and_actors = get_movies_and_actors(last_actor)
        return jsonify({
            "displayingActors": displaying_actors,
            "dict_of_movies_and_actors": dict_of_movies_and_actors
        })

    # Render HTML for direct browser requests
    displaying_actors = session.get("displaying_actors", [session.get("start_actor")])
    last_actor = displaying_actors[-1]
    dict_of_movies_and_actors = get_movies_and_actors(last_actor)
    # print(displaying_actors)
    # print(dict_of_movies_and_actors)
    return render_template("game.html", displaying_actors=displaying_actors, dict_of_movies_and_actors=dict_of_movies_and_actors)



if __name__ == "__main__":
    load_data("large")
    app.run(debug=True)
