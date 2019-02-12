# This file initializes your application and brings together all of the various components.
from flask import Flask
from backend.api.routes import api
from backend.upload.routes import upload
from flask_cors import CORS
import os

application = Flask(__name__)
if os.environ.get('FLASK_DEBUG'):
    CORS(application, origin='http://localhost:8080')

application.register_blueprint(api, url_prefix='/api')
application.register_blueprint(upload, url_prefix='/upload')
