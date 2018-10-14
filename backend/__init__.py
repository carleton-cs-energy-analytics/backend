# This file initializes your application and brings together all of the various components.
from flask import Flask
from backend.api.routes import api

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
