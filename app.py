from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('movie_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Get all movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])

# Get a single movie by ID
@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (id,)).fetchone()
    conn.close()
    if movie is None:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(dict(movie))

# Add a new movie
@app.route('/api/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    title = data['title']
    genre = data['genre']
    year = data.get('year', None)
    plot = data.get('plot', None)
    rating = data.get('rating', None)
    poster_url = data.get('poster_url', None)

    conn = get_db_connection()
    conn.execute('INSERT INTO movies (title, genre, year, plot, rating, poster_url) VALUES (?, ?, ?, ?, ?, ?)',
                 (title, genre, year, plot, rating, poster_url))
    conn.commit()
    conn.close()
    return jsonify({"message": "Movie added successfully!"}), 201

# Update movie details
@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    data = request.get_json()
    title = data['title']
    genre = data['genre']
    year = data.get('year', None)
    plot = data.get('plot', None)
    rating = data.get('rating', None)
    poster_url = data.get('poster_url', None)

    conn = get_db_connection()
    conn.execute('UPDATE movies SET title = ?, genre = ?, year = ?, plot = ?, rating = ?, poster_url = ? WHERE id = ?',
                 (title, genre, year, plot, rating, poster_url, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Movie updated successfully!"})

# Delete a movie
@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Movie deleted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
