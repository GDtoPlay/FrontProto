import os
from flask import Flask, request, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import *
from flask_migrate import Migrate
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/tozero13689/FrontProto/app/upload/test'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pcap'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
