import os
import psycopg2
from flask import jsonify

CONN = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')


def unwrap(result):
    return jsonify(result[0][0])


def query_json_array(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute("SELECT array_to_json(array_agg(row_to_json(a)))::TEXT FROM (" + query + ") AS a;", vars)
        result = curs.fetchall()
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]  # TODO: What about when there are no results? "[]" or error?


def query_json_item(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute("SELECT row_to_json(a)::TEXT FROM (" + query + ") AS a;", vars)
        result = curs.fetchall()
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]


class Buildings:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM buildings")

    @staticmethod
    def get(id):
        return query_json_item("SELECT * FROM buildings WHERE building_id = %s LIMIT 1", id)


class Rooms:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM rooms")

    @staticmethod
    def get(id):
        return query_json_item("SELECT * FROM rooms WHERE room_id = %s", id)


class Tags:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM tags")

    @staticmethod
    def get_id(id):
        return query_json_item("SELECT * FROM tags WHERE tag_id = %s", id)


class Devices:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM devices")

    @staticmethod
    def get_id(id):
        return query_json_item("SELECT * FROM devices WHERE device_id = %s", id)


class Points:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM points")

    @staticmethod
    def get_id(id):
        return query_json_item("SELECT * FROM points WHERE point_id = %s", id)


class Categories:
    @staticmethod
    def all():
        return query_json_array("SELECT * FROM categories")

    @staticmethod
    def get_id(id):
        return query_json_array("SELECT * FROM tags WHERE category_id = %s", id)