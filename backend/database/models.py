import os
import psycopg2
from flask import jsonify

CONN = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')


def unwrap(result):
    return jsonify(result[0][0])


def unwrap_tuple(result):
    result_list = []
    for tuple in result:
        result_list.append(tuple[0])

    return result_list


def query_json_array(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute(
            "SELECT array_to_json(array_agg(row_to_json(a)))::TEXT FROM (" + query + ") AS a;",
            vars)
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


def query_single_column(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        return unwrap_tuple(curs.fetchall())


def query_single_cell(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        result = curs.fetchall()
        print(type(result))
        print(result)
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]


def insert(query, vars=None):
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        CONN.commit()


class Buildings:
    sql_query = """
        SELECT building_id, name AS building_name,
            (SELECT
                ARRAY(SELECT name
                    FROM tags
                        INNER JOIN buildings_tags
                            ON tags.tag_id = buildings_tags.tag_id
                    WHERE buildings_tags.building_id = buildings.building_id)) AS tags
        FROM buildings
        """

    @staticmethod
    def all():
        return query_json_array(Buildings.sql_query)

    @staticmethod
    def get(id):
        return query_json_item(Buildings.sql_query + "WHERE buildings.building_id = %s", id)

    @staticmethod
    def where(where_clause):
        return query_json_array(Buildings.sql_query + where_clause)

    @staticmethod
    def ids_where(where_clause):
        base_query = """
            SELECT DISTINCT buildings.building_id 
            FROM buildings
                LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
        """

        return query_single_column(base_query + where_clause)


class Rooms:
    sql_query = """
        SELECT room_id,
           rooms.name AS room_name,
           rooms.building_id,
           buildings.name AS building_name,
           floor,
           rooms.description,
           (SELECT 
                ARRAY(SELECT name
                     FROM tags
                            INNER JOIN rooms_tags ON tags.tag_id = rooms_tags.tag_id
                     WHERE rooms_tags.room_id = rooms.room_id
                         UNION
                     SELECT name
                     FROM tags
                            INNER JOIN buildings_tags ON tags.tag_id = buildings_tags.tag_id
                     WHERE buildings_tags.building_id = buildings.building_id
                       )) AS tags
        FROM rooms
            LEFT JOIN buildings ON rooms.building_id = buildings.building_id
        """

    @staticmethod
    def all():
        return query_json_array(Rooms.sql_query)

    @staticmethod
    def get(id):
        return query_json_item(Rooms.sql_query + "WHERE room_id = %s", id)

    @staticmethod
    def where(where_clause):
        return query_json_array(Rooms.sql_query + where_clause)

    @staticmethod
    def ids_where(where_clause):
        base_query = """
                SELECT DISTINCT rooms.room_id
                FROM rooms
                    LEFT JOIN buildings ON rooms.building_id = buildings.building_id
                    LEFT JOIN rooms_tags ON rooms.room_id = rooms_tags.room_id
                    LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
        """

        return query_single_column(base_query + where_clause)


class Tags:
    sql_query = """
        SELECT tag_id,
           tags.name AS tag_name,
           tags.category_id,
           categories.name AS category_name,
           tags.description
        FROM tags
            LEFT JOIN categories ON tags.category_id = categories.category_id
        """

    @staticmethod
    def all():
        return query_json_array(Tags.sql_query)

    @staticmethod
    def get_id(id):
        return query_json_item(Tags.sql_query + "WHERE tag_id = %s", id)


class Devices:
    sql_query = """
        SELECT devices.device_id,
            devices.name AS device_name,
            rooms.room_id,
            rooms.name AS room_name,
            buildings.building_id,
            buildings.name AS building_name,
            (SELECT 
                ARRAY(SELECT name
                     FROM tags
                            INNER JOIN devices_tags ON tags.tag_id = devices_tags.tag_id
                     WHERE devices_tags.device_id = devices.device_id
                         UNION
                     SELECT name
                     FROM tags
                            INNER JOIN rooms_tags ON tags.tag_id = rooms_tags.tag_id
                     WHERE rooms_tags.room_id = rooms.room_id
                         UNION
                     SELECT name
                     FROM tags
                            INNER JOIN buildings_tags ON tags.tag_id = buildings_tags.tag_id
                     WHERE buildings_tags.building_id = buildings.building_id
                       )) AS tags,
            devices.description
        FROM devices
            LEFT JOIN rooms ON devices.room_id = rooms.room_id
            LEFT JOIN buildings ON rooms.building_id = buildings.building_id
        """

    @staticmethod
    def all():
        return query_json_array(Devices.sql_query)

    @staticmethod
    def get(id):
        return query_json_item(Devices.sql_query + "WHERE device_id = %s", id)

    @staticmethod
    def where(where_clause):
        return query_json_array(Devices.sql_query + where_clause)

    @staticmethod
    def ids_where(where_clause):
        base_query = """
                    SELECT DISTINCT devices.device_id
                    FROM devices
                        LEFT JOIN rooms ON devices.room_id = rooms.room_id
                        LEFT JOIN buildings ON rooms.building_id = buildings.building_id
                        LEFT JOIN devices_tags ON devices.device_id = devices_tags.device_id
                        LEFT JOIN rooms_tags ON rooms.room_id = rooms_tags.room_id
                        LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
            """

        return query_single_column(base_query + where_clause)


class Points:
    sql_query = """
        SELECT points.point_id, 
            points.name AS point_name,
            devices.device_id,
            devices.name AS device_name,
            rooms.room_id,
            rooms.name AS room_name,
            buildings.building_id,
            buildings.name AS building_name,
            (SELECT row_to_json(a) 
                FROM (SELECT value_type_id, storage_kind, enums.cases
                      FROM value_types
                            LEFT JOIN enums ON value_types.enum_id = enums.enum_id
                      WHERE value_types.value_type_id = points.value_type_id
            ) a) AS value_type,
            (SELECT row_to_json(a) 
                FROM (SELECT value_unit_id, measurement, unit 
                      FROM value_units
                      WHERE value_units.value_unit_id = points.value_unit_id
            ) a) AS value_unit,
            (SELECT 
                ARRAY (SELECT name
                       FROM tags
                              INNER JOIN points_tags ON tags.tag_id = points_tags.tag_id
                       WHERE points_tags.point_id = points.point_id
                       UNION
                       SELECT name
                       FROM tags
                              INNER JOIN devices_tags ON tags.tag_id = devices_tags.tag_id
                       WHERE devices_tags.device_id = devices.device_id
                       UNION
                       SELECT name
                       FROM tags
                              INNER JOIN rooms_tags ON tags.tag_id = rooms_tags.tag_id
                       WHERE rooms_tags.room_id = rooms.room_id
                       UNION
                       SELECT name
                       FROM tags
                              INNER JOIN buildings_tags ON tags.tag_id = buildings_tags.tag_id
                       WHERE buildings_tags.building_id = buildings.building_id)) AS tags,
            points.description
        FROM points
            LEFT JOIN devices ON points.device_id = devices.device_id
            LEFT JOIN rooms ON devices.room_id = rooms.room_id
            LEFT JOIN buildings ON rooms.building_id = buildings.building_id
        """

    @staticmethod
    def all():
        return query_json_array(Points.sql_query)

    @staticmethod
    def get(id):
        return query_json_item(Points.sql_query + "WHERE point_id = %s", id)

    @staticmethod
    def where(where_clause):
        return query_json_array(Points.sql_query + where_clause)

    @staticmethod
    def ids_where(where_clause):
        base_query = """
            SELECT DISTINCT points.point_id
            FROM points
                LEFT JOIN devices ON points.device_id = devices.device_id
                LEFT JOIN rooms ON devices.room_id = rooms.room_id
                LEFT JOIN buildings ON rooms.building_id = buildings.building_id
                LEFT JOIN value_units ON points.value_unit_id = value_units.value_unit_id
                LEFT JOIN points_tags ON points.point_id = points_tags.point_id
                LEFT JOIN devices_tags ON devices.device_id = devices_tags.device_id
                LEFT JOIN rooms_tags ON rooms.room_id = rooms_tags.room_id
                LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
            """
        return query_single_column(base_query + where_clause)

    @staticmethod
    def value_is_double(id):
        storage_kind = query_single_cell("""
            SELECT storage_kind
            FROM value_types
                INNER JOIN points ON value_types.value_type_id = points.value_type_id
            WHERE point_id = %s
            ;""", id)
        return storage_kind == 'double'


class Categories:
    sql_query = "SELECT categories.category_id, categories.name AS category_name FROM categories "

    @staticmethod
    def all():
        return query_json_array(Categories.sql_query)

    @staticmethod
    def get_id(id):
        return query_json_item(Categories.sql_query + "WHERE category_id = %s", id)


class Values:
    @staticmethod
    def add(point_id, timestamp, value):
        value_is_double = Points.value_is_double(point_id)
        if value_is_double:
            insert("""
            INSERT INTO values (point_id, timestamp, double) VALUES (%s, %s, %s);
            """, (point_id, timestamp, value))
        else:
            insert("""
            INSERT INTO values (point_id, timestamp, int) VALUES (%s, %s, %s);
            """, (point_id, timestamp, value))

    @staticmethod
    def get(point_ids, start_time, end_time):
        return query_json_array("""
            SELECT value_id, points.name AS point_name, timestamp, int AS value
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
            WHERE int IS NOT NULL
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            UNION
            SELECT value_id, points.name AS point_name, timestamp, double AS value
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
            WHERE double IS NOT NULL
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            """, (point_ids, start_time, end_time, point_ids, start_time, end_time))
