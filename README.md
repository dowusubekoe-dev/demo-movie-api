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


