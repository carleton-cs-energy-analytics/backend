from flask import Blueprint, request, abort
from backend.database.models import *
from backend.database.Search import Search
from backend.database.exceptions import *

api = Blueprint('api', __name__)


@api.route('/points')
def get_points():
    if request.args.get('search'):
        try:
            return Points.where(Search.points(request.args.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Points.all() or "[]"


@api.route('/point/<id>')
def get_point_by_id(id):
    return Points.get_by_id(id) or "[]"


@api.route('/devices')
def get_devices():
    if request.args.get('search'):
        try:
            return Devices.where(Search.devices(request.args.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Devices.all() or "[]"


@api.route('/device/<id>')
def get_device_by_id(id):
    return Devices.get_by_id(id) or "[]"


@api.route('/rooms')
def get_rooms():
    if request.args.get('search'):
        try:
            return Rooms.where(Search.rooms(request.args.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Rooms.all() or "[]"


@api.route('/room/<id>')
def get_room(id):
    return Rooms.get_by_id(id) or "[]"


@api.route('/buildings')
def get_buildings():
    if request.args.get('search'):
        try:
            return Buildings.where(Search.buildings(request.args.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Buildings.all() or "[]"


@api.route('/building/<id>')
def get_building(id):
    return Buildings.get_by_id(id) or "[]"


@api.route('/building/<id>/floors')
def get_floors_by_building_id(id):
    return Buildings.floors(id) or "[]"


@api.route('/all_floors')  # This name is bad and inconsistent, but we have bigger fish to fry
def get_all_floors():
    return Buildings.all_floors() or "[]"


@api.route('/tags')
def get_all_tags():
    return Tags.all() or "[]"


@api.route('/tag/<id>')
def get_tag_by_id(id):
    return Tags.get_by_id(id) or "[]"


@api.route('/categories')
def get_all_categories():
    return Categories.all() or "[]"


@api.route('/category/<id>')
def get_tags_by_category_id(id):
    return Categories.get_by_id(id) or "[]"


@api.route('/units')
def get_all_units():
    return Units.all() or "[]"


@api.route('/unit/<id>')
def get_unit_by_id(id):
    return Units.get_by_id(id) or "[]"


@api.route('/types')
def get_all_types():
    return Types.all() or "[]"


@api.route('/type/<id>')
def get_type_by_id(id):
    return Types.get_by_id(id) or "[]"


@api.route('/values', methods=['GET'])
def get_values():
    point_ids = request.args.getlist('point_ids') or request.args.getlist('point_ids[]')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    search = request.args.get('search')

    return Values.get(tuple(point_ids), start_time, end_time, Search.values(search)) or "[]"


@api.route('/values', methods=['POST'])
def post_values():
    Values.add(request.get_json())

    return "Success"


@api.route('/points/verify')
def search_verify():
    if request.args.get("search") is None:
        abort(400, "Request must include a `search` argument")
    try:
        return Points.counts_where(Search.points(request.args.get("search"))) or "[]"
    except psycopg2.Error as e:  # Any InvalidSearchException will be thrown and result in a 500.
        return "Invalid Point Search: " + str(e.pgerror)


@api.route('/values/verify')
def values_verify():
    if request.args.get("search") is None:
        abort(400, "Request must include a `search` argument")
    try:
        Search.values(request.args.get("search"))
    except psycopg2.Error as e:  # Any InvalidSearchException will be thrown and result in a 500.
        return "Invalid Value Search: " + str(e.pgerror)
    return "Valid"
