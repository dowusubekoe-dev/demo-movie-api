# Simple REST API locally on a Linux server using Python with the Flask Framework

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
    app.run(host='0.0.0.0', port=5000, debug=True)
```

5. Run the API Server
Start the Flask API server by running:

```bash
python3 app.py
```
By default, Flask will start the server on port 5000.
