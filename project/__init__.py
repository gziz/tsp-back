import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")

cors = CORS(app, origins=["*"])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from project.locations.views import locations_blueprint
app.register_blueprint(locations_blueprint, url_prefix='/locations')
