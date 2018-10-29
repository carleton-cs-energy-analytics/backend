from flask import Blueprint
from backend.database.models import *

api = Blueprint('api', __name__)


@api.route('/buildings')
def get_all_buildings():
    return Buildings.all()


@api.route('/building/<id>')
def get_building(id):
    return Buildings.get(id)


@api.route('/rooms')
def get_all_rooms():
    return Rooms.all()


@api.route('/room/<id>')
def get_room(id):
    return Rooms.get(id)


@api.route('/tags')
def get_all_tags():
    return Tags.all()


@api.route('/tag/<id>')
def get_tag_by_id(id):
    return Tags.get(id)


@api.route('/devices')
def get_all_devices():
    return Devices.all()


@api.route('/device/<id>')
def get_device_by_id(id):
    return Devices.get(id)


@api.route('/points')
def get_all_points():
    return Points.all()


@api.route('/point/<id>')
def get_point_by_id(id):
    return Points.get(id)


@api.route('/categories')
def get_all_categories():
    return Categories.all()


@api.route('/category/<id>')
def get_tags_by_category_id(id):
    return Categories.get_id(id)
