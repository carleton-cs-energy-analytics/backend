from flask import Blueprint, request, abort, jsonify
from backend.database.models import *
from backend.database.Search import Search
from backend.database.exceptions import *
import datetime as dt

api = Blueprint('api', __name__)


@api.route('/points', methods=['GET', 'POST'])
def get_points():
    if request.values.get('search'):
        try:
            return Points.where(Search.points(request.values.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Points.all() or "[]"


@api.route('/points/ids', methods=['GET', 'POST'])
def get_points_ids():
    if not request.values.get('search'):
        abort(400, "Must include search paramter")

    try:
        return jsonify(Points.ids_where(Search.points(request.values.get('search')))) or "[]"
    except InvalidSearchException as e:
        abort(400, e)


@api.route('/point/<id>')
def get_point_by_id(id):
    return Points.get_by_id(id) or "[]"


@api.route('/devices', methods=['GET', 'POST'])
def get_devices():
    if request.values.get('search'):
        try:
            return Devices.where(Search.devices(request.values.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Devices.all() or "[]"


@api.route('/device/<id>')
def get_device_by_id(id):
    return Devices.get_by_id(id) or "[]"


@api.route('/rooms', methods=['GET', 'POST'])
def get_rooms():
    if request.values.get('search'):
        try:
            return Rooms.where(Search.rooms(request.values.get('search'))) or "[]"
        except InvalidSearchException as e:
            abort(400, e)
    else:
        return Rooms.all() or "[]"


@api.route('/room/<id>')
def get_room(id):
    return Rooms.get_by_id(id) or "[]"


@api.route('/buildings', methods=['GET', 'POST'])
def get_buildings():
    if request.values.get('search'):
        try:
            return Buildings.where(Search.buildings(request.values.get('search'))) or "[]"
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


@api.route('/measurements')
def get_all_measurements():
    return Units.get_all_measurements() or "[]"


@api.route('/types')
def get_all_types():
    return Types.all() or "[]"


@api.route('/type/<id>')
def get_type_by_id(id):
    return Types.get_by_id(id) or "[]"


@api.route('/values', methods=['GET', 'POST'])
def get_values():
    point_ids = request.values.getlist('point_ids') or request.values.getlist('point_ids[]')
    start_time = request.values.get('start_time')
    end_time = request.values.get('end_time')

    search = request.values.get('search')

    search_sql = Search.values(search)
    print("search", search)
    print("sql", search_sql)

    return Values.get(tuple(point_ids), start_time, end_time, search_sql) or "[]"


@api.route('/values/add', methods=['POST'])
def post_values():
    json = request.get_json()
    if Values.exists(json[0][0], json[0][1]):
        return "File already imported", 204
    Values.add(json)

    return "Success"


@api.route('/points/verify', methods=['GET', 'POST'])
def search_verify():
    if request.values.get("search") is None:
        abort(400, "Request must include a `search` argument")
    try:
        return Points.counts_where(Search.points(request.values.get("search"))) or "[]"
    except psycopg2.Error as e:  # Any InvalidSearchException will be thrown and result in a 500.
        return "Invalid Point Search: " + str(e.pgerror)


@api.route('/values/verify', methods=['GET', 'POST'])
def values_verify():
    if request.values.get("search") is None:
        abort(400, "Request must include a `search` argument")
    try:
        point_ids = request.values.getlist('point_ids') or request.values.getlist('point_ids[]')
        start_time = request.values.get('start_time')
        end_time = request.values.get('end_time')

        search = request.values.get('search')
        search_sql = Search.values(search)

        return "%s values found" % Values.get_count(tuple(point_ids), start_time, end_time,
                                                    search_sql)
    except InvalidSearchException:
        return "Invalid Value Search Syntax"
    except psycopg2.Error as e:  # Any InvalidSearchException will be thrown and result in a 500.
        return "Invalid Value Search: " + str(e.pgerror)


@api.route('/rules')
def get_all_rules():
    return Rules.all() or "[]"


@api.route('/rule/<id>')
def get_rule_by_id(id):
    return Rules.get_by_id(id) or "[]"


def trycast_int(obj):
    try:
        return int(obj)
    except (TypeError, ValueError):
        return None


@api.route('/rule/<id>/count')
def get_rule_count(id):
    since = trycast_int(request.values.get("since"))
    start_time = trycast_int(request.values.get("start_time"))
    end_time = trycast_int(request.values.get("end_time"))
    if since is not None:
        start = since
        end = int(dt.datetime.now().timestamp())
    elif None not in (start_time, end_time):
        start = start_time
        end = end_time
    else:
        end = int(dt.datetime.combine(dt.date.today(), dt.time()).timestamp())
        start = end - 60*60*24

    if not Values.has_any_since(start):
        abort(404, "No values since start time %s" % start)

    (point_search, value_search) = Rules.searches(id)
    point_ids = Points.ids_where(Search.points(point_search))

    return str(Values.get_count(point_ids, start, end, Search.values(value_search)))


@api.route('/rule/<id>/matches')
def get_rule_matches(id):
    since = trycast_int(request.values.get("since"))
    start_time = trycast_int(request.values.get("start_time"))
    end_time = trycast_int(request.values.get("end_time"))
    if since is not None:
        start = since
        end = int(dt.datetime.now().timestamp())
    elif None not in (start_time, end_time):
        start = start_time
        end = end_time
    else:
        end = int(dt.datetime.combine(dt.date.today(), dt.time()).timestamp())
        start = end - 60*60*24

    if not Values.has_any_since(start):
        abort(404, "No values since start time %s" % start)

    (point_search, value_search) = Rules.searches(id)
    point_ids = Points.ids_where(Search.points(point_search))

    return Values.get(point_ids, start, end, Search.values(value_search))


@api.route('/rule/add', methods=['POST'])
def post_rule_add():
    name = request.values.get("name")
    url = request.values.get("url")
    point_search = request.values.get("point_search")
    value_search = request.values.get("value_search")
    if None in (name, url, point_search, value_search):
        abort(400)
    Rules.add(name, url, point_search, value_search)
    return "Success"


@api.route('/rule/<id>/delete', methods=['POST'])
def post_rule_remove(id):
    Rules.delete(id)
    return "Success"


@api.route('/rule/<id>/rename', methods=['POST'])
def post_rule_rename(id):
    name = request.values.get("name")
    if name is None:
        abort(400)
    return Rules.rename(id, name)
