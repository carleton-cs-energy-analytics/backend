from flask import Blueprint
from backend.database.models import *

api = Blueprint('api', __name__)


@api.route('/buildings')
def get_all_buildings():
    try:
        return Buildings.all()

    except Exception as e:
        # TODO: do something with exceptions
        raise e


@api.route('/building/<id>')
def get_building(id):
    return Buildings.get(id)


@api.route('/rooms')
def get_all_rooms():
    try:
        return Rooms.all()

    except Exception as e:
        # TODO: do something with exceptions
        raise e


@api.route('/room/<id>')
def get_room(id):
    return Rooms.get(id)


@api.route('/tags')
def get_all_tags():
    try:
        return Tags.all()

    except Exception as e:
        # TODO: do something with exceptions
        raise e


@api.route('/tag/<id>')
def get_tag_by_id(id):
    return Tags.get_id(id)


@api.route('/devices')
def get_all_devices():
    try:
        return Devices.all()

    except Exception as e:
        raise e


@api.route('/device/<id>')
def get_device_by_id(id):
    return Devices.get_id(id)


@api.route('/points')
def get_all_points():
    try:
        return Points.all()

    except Exception as e:
        raise e
