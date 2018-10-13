# This file initializes your application and brings together all of the various components.
from flask import Flask

app = Flask(__name__)

app.register_blueprint(api, urlprefix='/api')