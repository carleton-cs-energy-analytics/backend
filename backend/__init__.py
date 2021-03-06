# This file initializes your application and brings together all of the various components.
from flask import Flask
from backend.api.routes import api
from backend.upload.routes import upload
from flask_cors import CORS

application = Flask(__name__)

CORS(application, origin='*')

application.register_blueprint(api, url_prefix='/api')
application.register_blueprint(upload, url_prefix='/upload')
