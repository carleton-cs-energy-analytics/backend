import os
from flask import Blueprint, request, abort
from werkzeug.utils import secure_filename

api = Blueprint('upload', __name__)


@api.route('siemens', methods=['POST'])
def upload_siemens():
    upload('siemens')


@api.route('alc', methods=['POST'])
def upload_alc():
    upload('alc')


def upload(directory):
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']

    if file.filename == '':
        abort(400)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('/var/data/uploads/', directory, filename))
