from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/health/full")
def health_check():
    return json.dumps({"status" : "healthy", "response": 200})