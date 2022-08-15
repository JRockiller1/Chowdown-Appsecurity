from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyotp
from flask_bootstrap import Bootstrap
from flask import *

# Creates the application object 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lablam.2017'
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LdeeRwhAAAAACbV8SReJ9bNsV7-QBLU9tnOewGB'
app.config['RECAPTCHA_PRIVATE_KEY']='6LdeeRwhAAAAADGrXiD334_nupZoMB5OLCd1yH-M'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}

Bootstrap(app)

app.static_folder='static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chowdown1.db'
db = SQLAlchemy(app)


# Import Views from the app module. (DO NOT Confuse with app variable)
from app import views
# from app import baseAccount
# Import is at the end to avoid circular reference
