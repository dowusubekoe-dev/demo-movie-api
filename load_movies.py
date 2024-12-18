import sqlite3
import json

# Connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect('movie_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Load movies from JSON file
def load_movies_from_json(file_path):
    with open(file_path, 'r') as file:
        movies = json.load(file)
    return movies

# Insert movies into the database
def insert_movies(movies):
    conn = get_db_connection()
    for movie in movies:
        conn.execute('''
            INSERT INTO movies (title, genre, year, plot, rating, poster_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (movie['title'], movie['genre'], movie['year'], movie['plot'], movie['rating'], movie['poster_url']))
    conn.commit()
    conn.close()

# Main function to load the movies
def main():
    movies = load_movies_from_json('movies.json')
    insert_movies(movies)
    print(f'{len(movies)} movies loaded successfully!')

if __name__ == '__main__':
    main()
