from flask import Flask
from flask_cors import CORS

# Initialize the app
app = Flask("__name__")
CORS(app)


# Load the views
from app.views import app


