# This file initializes your application and brings together all of the various components.
from flask import Flask
from backend.api.routes import api

application = Flask(__name__)

application.register_blueprint(api, url_prefix='/api')
