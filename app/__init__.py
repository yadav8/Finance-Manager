from flask import Flask
from config import Config

# Creating a flask instace - app
app = Flask(__name__) 
app.config.from_object(Config)

# The 'app' folder
from app import routes
