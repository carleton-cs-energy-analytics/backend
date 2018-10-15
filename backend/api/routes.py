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
