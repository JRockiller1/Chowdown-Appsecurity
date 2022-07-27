from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Creates the application object 
app = Flask(__name__)

app.static_folder='static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chowdown1.db'
db = SQLAlchemy(app)


# Import Views from the app module. (DO NOT Confuse with app variable)
from app import views
# from app import baseAccount
# Import is at the end to avoid circular reference
