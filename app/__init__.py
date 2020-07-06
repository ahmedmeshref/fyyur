# Imports

from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate
from flask_compress import Compress

# App Config.

app = Flask(__name__)
Compress(app)
moment = Moment(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes





