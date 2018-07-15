import os
from flask import Flask, request, redirect, url_for
from config import Config
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = '/home/tozero13689/FrontProto/app/upload/test'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pcap'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:key13689@localhost:3306/temp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes, models
