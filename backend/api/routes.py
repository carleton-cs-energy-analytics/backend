from flask import Blueprint, request
from backend.database.models import *
from backend.database.Search import Search

api = Blueprint('api', __name__)


@api.route('/points')
def get_points():
    if request.args.get('search'):
        Points.where(Search.points(request.args.get('search')))
    else:
        return Points.all()


@api.route('/point/<id>')
def get_point_by_id(id):
    return Points.get_by_id(id)


@api.route('/devices')
def get_devices():
    if request.args.get('search'):
        Devices.where(Search.devices(request.args.get('search')))
    else:
        return Devices.all()


@api.route('/device/<id>')
def get_device_by_id(id):
    return Devices.get_by_id(id)


@api.route('/rooms')
def get_rooms():
    if request.args.get('search'):
        Rooms.where(Search.rooms(request.args.get('search')))
    else:
        return Rooms.all()


@api.route('/room/<id>')
def get_room(id):
    return Rooms.get_by_id(id)


@api.route('/buildings')
def get_buildings():
    if request.args.get('search'):
        return Buildings.where(Search.buildings(request.args.get('search')))
    else:
        return Buildings.all()


@api.route('/building/<id>')
def get_building(id):
    return Buildings.get_by_id(id)


@api.route('/tags')
def get_all_tags():
    return Tags.all()


@api.route('/tag/<id>')
def get_tag_by_id(id):
    return Tags.get_by_id(id)


@api.route('/categories')
def get_all_categories():
    return Categories.all()


@api.route('/category/<id>')
def get_tags_by_category_id(id):
    return Categories.get_by_id(id)


@api.route('/values', methods=['GET'])
def get_values():
    point_ids = request.args.getlist('point_ids')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    return Values.get(tuple(point_ids), start_time, end_time)


@api.route('/values', methods=['POST'])
def post_values():
    Values.add(request.get_json())

    return "Success"
