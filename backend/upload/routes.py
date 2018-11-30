import os
from flask import Blueprint, request, abort
from werkzeug.utils import secure_filename

upload = Blueprint('upload', __name__)

@upload.route('/')
def upload_home():
    return 'upload service is running'

@upload.route('siemens', methods=['POST'])
def upload_siemens():
    return upload_file_to_directory('siemens')

@upload.route('alc', methods=['POST'])
def upload_alc():
    return upload_file_to_directory('alc')

def upload_file_to_directory(directory):
    if 'file' not in request.files:
        abort(400)
    file_to_save = request.files['file']
    if file_to_save.filename == '':
        abort(400)
    if file_to_save:
        filename = secure_filename(file_to_save.filename)
        try:
            file_to_save.save(os.path.join('/var/data/uploads/', directory, filename))
        except:
            abort(403)
    return 'OK'
