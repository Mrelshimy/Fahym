from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Create a Flask application
app = Flask(__name__)

# Load the Config class into the Flask app
app.config.from_object(Config)

# Create a database instance
db = SQLAlchemy(app)
