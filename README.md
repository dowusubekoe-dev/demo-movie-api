# Simple REST API locally on a Linux server using Python with the Flask Framework (Dev)

## Prerequisites:
1. Linux server (local or remote).
2. Python (version 3.x).
3. pip (Python's package installer).

### Steps to Build the API:

1. Install Required Tools
Open the terminal on your Linux server and run:

```bash
# Install Python3 and pip if not already installed
sudo apt update
sudo apt install python3 python3-pip -y
```

2. Install Flask
Use pip to install Flask:

```bash
pip3 install flask
```

3. Create the API Project Directory
Navigate to your preferred folder and create a new project directory:

```bash
mkdir my_api
cd my_api
```

4. Write the API Code
Open the app.py file using a text editor (like nano, vim, or VSCode), and paste the following code:

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Root Endpoint
@app.route('/')
def home():
    return jsonify({"message": "Welcome to my API!"})

# Simple GET Endpoint
@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({"greeting": f"Hello, {name}!"})

# Simple POST Endpoint
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({"received_data": data})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
```

5. Run the API Server
Start the Flask API server by running:

```bash
python3 app.py
```
By default, Flask will start the server on port 5000. But for this app I used port 5002 because I had a docker image also running on port 5000
Ensure port 5002 is open in your firewall settings.

```bash
sudo ufw allow 5002
```

### Test the API

**a) Test the Root Endpoint** 
Open your browser or use curl:

```bash
curl http://127.0.0.1:5002/
```
Expected Output:

```json
{"message": "Welcome to my API!"}
```

**b) Test the GET Endpoint with Query Parameters**

```bash
curl "http://127.0.0.1:5002/api/greet?name=John"
```

Expected Output:

```json
{"greeting": "Hello, John!"}
```

**c) Test the POST Locally** 

Use curl to send JSON data:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://127.0.0.1:5002/api/echo
```

Expected Output:

```json
{"received_data": {"key": "value"}}
```

Stop the Server
To stop the server, press Ctrl + C.

### Test the API

To access the data from the movie database, **routes** will be used and to test if the app works and make it accessible to other devices on the same network, a route to display a simple message is used.

```python
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API!"})
```
By default, Flask binds to 127.0.0.1 (localhost), which means it only listens for requests from the same machine. To allow external access, ensure the host is set to 0.0.0.0 in your app.run():

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
```
This change makes Flask listen on all network interfaces, including the machine that the app is running on. E.g a linux server.


#### Final code for testing the app.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
```

1. To set the api internally, run

```bash
python3 app.py
```
Click on the link by using Ctrl + Click or copy URL and paste in the browser. test root endpoint using this command

Expected output:

![](./images/test-api.PNG)


2. For externnal testing of the api, using **curl**

```bash
curl http://127.0.0.1:5002/
```
Expected output:

```bash
$ curl http://19x.xxx.xxx.xxx:5002
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    45  100    45    0     0   2502      0 --:--:-- --:--:-- --:--:--  2647
{
  "message": "Welcome to the Flask API!"
}
```
This section helped to get a better understanding of how set up APIs locally or externally and run the POST and GET requests or use **curl** command.

---


#  Prepare Flask API for Production using SQLite, Gunicorn, Nginx and Docker

For this section, I will be looking into how to store the movie data to a database and modify the **app.py** to add **routes** for *adding*, *viewing*, and *updating* movie data.


## Run Flask API with Gunicorn (Production WSGI Server)

1. Install **Gunicorn**
First, install Gunicorn using pip3

```bash
pip3 install gunicorn
```

2. Run Gunicorn with Flask
Navigate to your project directory (where app.py is located) and run

```bash
gunicorn --bind 0.0.0.0:5002 app:app
```
Explanation:
- app before : is the filename (app.py)
- app after : is the Flask instance created in the file

---


## Set Up Nginx as a Reverse Proxy

1. Install **Nginx**
Install Nginx on the Linux server

```bash
sudo apt update
sudo apt install nginx -y
```

2. Configure Nginx
Create a new Nginx configuration file for your Flask app

```bash
sudo nano /etc/nginx/sites-available/flask_api
```
Add the following configuration

```nginx
server {
    listen 80;
    server_name your_server_ip_or_domain;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Replace:
- ****your_server_ip_or_domain** with the linux server ip address

3. Enable the Configuration
Run the following commands

```bash
sudo ln -s /etc/nginx/sites-available/flask_api /etc/nginx/sites-enabled/
sudo nginx -t  # Test Nginx configuration
sudo systemctl restart nginx
```
---


## Run Flask App with Gunicorn as a Service

To keep your Gunicorn app running, create a systemd service:

1. Create the service file

```bash
sudo nano /etc/systemd/system/flask_api.service
```

2. Add the following configuration

```ini
[Unit]
Description=Gunicorn instance to serve Flask API
After=network.target

[Service]
User=<your_linux_username>
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/usr/bin"
ExecStart=/usr/local/bin/gunicorn --workers 3 --bind unix:flask_api.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```
Replace:
- **your_linux_username** with your Linux user.
- **/path/to/your/project** with the absolute path to your Flask project.

3. Start and enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl start flask_api
sudo systemctl enable flask_api
```

4. Check the service status

```bash
sudo systemctl status flask_api
```
---


## Dockerize the Flask API

1. Create a Dockerfile
In **your project directory**, create a **Dockerfile**

```Dockerfile
# Use official Python image
FROM python:3.10
# Set working directory
WORKDIR /app
# Copy project files
COPY . /app
# Install dependencies
RUN pip install --no-cache-dir flask gunicorn
# Expose the port Flask uses
EXPOSE 5000
# Run the API with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]
```

2. Build the Docker Image
Run the following command in **your project directory**

```bash
docker build -t flask_api .
```

3. Run the Docker Container
Run the container to expose port 5002 or your the port of the app

```bash
docker run -d -p 5002:5002 flask_api
```

Test the API with;

```bash
curl http://127.0.0.1:5002/ # internally
```
OR

```bash
curl http://1xx.1xx.xx.xxx:5002/ # externally
```

---


## Connect Dockerized API to Nginx

For simplicity, I decided to run both **Nginx** and **Docker** on the same machine.

1. Modify the Nginx configuration **(/etc/nginx/sites-available/flask_api)**

```nginx
location / {
    proxy_pass http://127.0.0.1:5002;
}
```

2. Restart Nginx

```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```
In this section, I configured Flask to run with Gunicorn, set up Nginx as a reverse proxy and containerized the API with Docker for portability.

---


## Reload Systemd, Restart Service

Once the change is made:

```bash
sudo systemctl daemon-reload
sudo systemctl restart flask_api
```

Check the status of the service:

```bash
sudo systemctl status flask_api
```
---


## Test Endpoint in Postman

Assuming your Nginx is reverse-proxying requests to the Gunicorn API, test it via your server's IP address or domain name.

**a) Test the Root Endpoint**
Run the following command

```bash
curl http://<your_server_ip_or_domain>/ # You should see the response: {"message": "Welcome to my API!"}
```

**b) Test the GET Endpoint with Query Parameters**

```bash
curl "http://<your_server_ip_or_domain>:<port>/api/greet?name=John" # {"greeting": "Hello, John!"}
```

**c) Test the POST Endpoint**
Send JSON data to the API

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "value"}' http://<your_server_ip_or_domain>/api/echo # {"received_data": {"key": "value"}}
```

### Test with Postman

1. Download and open Postman (or use its web version).
2. Create a new request:
    - Method: GET or POST
    - URL: http://<your_server_ip_or_domain>/api/greet or any other endpoint.
3. For the POST endpoint, go to Body > raw and set the type to JSON, then provide input:

```json
{"key": "value"}
```
4. Send the request and view the response

### Test with a Browser

1. For GET endpoints like / or /api/greet, open the browser and enter

```bash
http://<your_server_ip_or_domain>/
```

2. For /api/greet with query parameters

```perl
http://<your_server_ip_or_domain>/api/greet?name=John
```

---


## Plan Structure of Movie Data API

Structure of the API will need the following information

- Movie title
- Genre
- Release year
- Cast and crew
- Plot synopsis
- Ratings
- Poster image URL

### Import Flask, Python and SQLite Dependencies

Since I will be using using Python in buidling this app, I have to import Flask, jsonify, sqlit, and request from Flask.

```python
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
```

### Set Up Database

Use a database (like SQLite, PostgreSQL, or MySQL) to store your movie data. For simplicity, you can start with SQLite since it requires minimal setup.

1. Install SQLite

```bash
sudo apt-get install sqlite3
```
2. Create a Database Schema called (e.g movie_data.db)

```bash
sqlite3 movie_data.db
```
3. Create a basic table for the movie_data.db database

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    year INTEGER,
    plot TEXT,
    rating REAL,
    poster_url TEXT
);
```

### Connection to the SQLite Database

Create a function to connet to sqlite database.

```python
# Connect to SQLite DB
def get_db_connection():
    conn = sqlite3.connect('movie_data.db')
    conn.row_factory = sqlite3.Row
    return conn
```

### Route to Fetch all Movie Data

Create another route and function in app.py to pull movie data from the database.

```python
@app.route('/api/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    conn.close()
    return jsonify([dict(movie) for movie in movies])
```

### Request Movie Data by ID

```python
@app.route('/api/movies/<int:id>', methods=['GET'])
def get_movie(id):
    conn = get_db_connection()
    movie = conn.execute('SELECT * FROM movies WHERE id = ?', (id,)).fetchone()
    conn.close()
    if movie is None:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(dict(movie))
```

### Add New Movie Data to SQLite Database

```python
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
```

### Update Existing Movie Details

```python
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
```

### Delete Movie Data by ID

```python
@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Movie deleted successfully!"})
```

....


---


## Test the Movie API

1. **GET all movies:**

```bash
curl http://127.0.0.1:5002/api/movies
```

2. **GET a Movie by ID**

```bash
curl http://127.0.0.1:5002/api/movies/1
```

3. **POST a new moview**

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "title": "Inception",
  "genre": "Sci-Fi",
  "year": 2010,
  "plot": "A mind-bending thriller.",
  "rating": 8.8,
  "poster_url": "https://link_to_poster.com"
}' http://127.0.0.1:5002/api/movies
```

4. **PUT to update a movie**

```bash
curl -X PUT -H "Content-Type: application/json" -d '{
  "title": "Inception",
  "genre": "Sci-Fi",
  "year": 2010,
  "plot": "A new plot description.",
  "rating": 9.0,
  "poster_url": "https://new_link_to_poster.com"
}' http://127.0.0.1:5000/api/movies/1
```
5. **DELETE a movie**

```bash
curl -X DELETE http://127.0.0.1:5002/api/movies/1
```

---









