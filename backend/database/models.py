import os
import psycopg2
from flask import jsonify

CONN = psycopg2.connect(dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')


def unwrap_tuple(tuples):
    """Maps a list of tuples to a list of the first element of the tuples.

    :param tuples: A list of tuples
    :return: A list of the first elements of the tuples in the input list
    """
    items = []
    for tuple in tuples:
        items.append(tuple[0])

    return items


def query_json_array(query, vars=None):
    """Returns a JSON-encoded string of the results of the given SQL query.

    The query is wrapped a PostgreSQL `json_agg` function, the database query is issued, and then
    the results of the query are unwrapped to get the JSON-encoded string itself.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: A string containing the JSON-encoded results of the query
    """
    with CONN.cursor() as curs:
        curs.execute("SELECT json_agg(a)::TEXT FROM (" + query + ") AS a;", vars)
        result = curs.fetchall()
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]  # TODO: What about when there are no results? "[]" or error?


def query_json_item(query, vars=None):
    """Returns a JSON-encoded string of the single result of the given SQL query.

    The query is wrapped a PostgreSQL `row_to_json` function, the database query is issued, and then
    the results of the query are unwrapped to get the JSON-encoded string itself.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: A string containing the JSON-encoded result of the query
    """
    with CONN.cursor() as curs:
        curs.execute("SELECT row_to_json(a)::TEXT FROM (" + query + ") AS a;", vars)
        result = curs.fetchall()
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]


def query_single_column(query, vars=None):
    """Takes a SQL query whose result is a single column, and returns the values of that column as a
    list.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: A list of the values in the single column of the result table
    """
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        return unwrap_tuple(curs.fetchall())


def query_single_cell(query, vars=None):
    """ Takes a SQL query whose result is a single cell, and returns the value in that cell.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: The value of the single cell of the result of the query
    """
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        result = curs.fetchall()
        if len(result) == 0:
            return None
        assert len(result) == 1
        assert len(result[0]) == 1
        return result[0][0]


def query_single_row(query, vars=None):
    """ Takes a SQL query whose result is a single row, and returns the values in that row.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: The value of the single row of the result of the query
    """
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        result = curs.fetchall()
        if len(result) == 0:
            return None
        assert len(result) == 1
        return result[0]


def insert(query, vars=None):
    """Runs the given query on the database, then commits the database connection.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    """
    with CONN.cursor() as curs:
        curs.execute(query, vars)
        CONN.commit()


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
                FROM (SELECT value_type_id, type
                      FROM value_types
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
        """Returns a JSON-encoded array of all Points."""
        return query_json_array(Points.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Point whose id is that given."""
        return query_json_item(Points.sql_query + "WHERE point_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Points whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Points.sql_query + "WHERE point_id IN %s", (tuple(ids),))

    @staticmethod
    def where(where_clause):
        """Returns a JSON-encoded array of all Points which match the given WHERE-clause."""
        ids = Points.ids_where(where_clause)
        return Points.get_by_ids(ids)

    @staticmethod
    def ids_where(where_clause):
        """Returns a list of the ids of all Points which match the given WHERE-clause."""
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
        """Returns a JSON-encoded array of all Devices."""
        return query_json_array(Devices.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Device whose id is that given."""
        return query_json_item(Devices.sql_query + "WHERE device_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Device whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Devices.sql_query + "WHERE device_id IN %s", (tuple(ids),))

    @staticmethod
    def where(where_clause):
        """Returns a JSON-encoded array of all Devices which match the given WHERE-clause."""
        ids = Devices.ids_where(where_clause)
        return Devices.get_by_ids(ids)

    @staticmethod
    def ids_where(where_clause):
        """Returns a list of the ids of all Devices which match the given WHERE-clause."""
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
        """Returns a JSON-encoded array of all Rooms."""
        return query_json_array(Rooms.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Room whose id is that given."""
        return query_json_item(Rooms.sql_query + "WHERE room_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Rooms whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Rooms.sql_query + "WHERE room_id IN %s", (tuple(ids),))

    @staticmethod
    def where(where_clause):
        """Returns a JSON-encoded array of all Rooms which match the given WHERE-clause."""
        ids = Rooms.ids_where(where_clause)
        return Rooms.get_by_ids(ids)

    @staticmethod
    def ids_where(where_clause):
        """Returns a list of the ids of all Rooms which match the given WHERE-clause."""
        base_query = """
                SELECT DISTINCT rooms.room_id
                FROM rooms
                    LEFT JOIN buildings ON rooms.building_id = buildings.building_id
                    LEFT JOIN rooms_tags ON rooms.room_id = rooms_tags.room_id
                    LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
        """

        return query_single_column(base_query + where_clause)


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
        """Returns a JSON-encoded array of all Buildings."""
        return query_json_array(Buildings.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Building whose id is that given."""
        return query_json_item(Buildings.sql_query + "WHERE buildings.building_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Buildings whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Buildings.sql_query + "WHERE building_id IN %s", (tuple(ids),))

    @staticmethod
    def where(where_clause):
        """Returns a JSON-encoded array of all Buildings which match the given WHERE-clause."""
        ids = Buildings.ids_where(where_clause)
        return Buildings.get_by_ids(ids)

    @staticmethod
    def ids_where(where_clause):
        """Returns a list of the ids of all Buildings which match the given WHERE-clause."""
        base_query = """
            SELECT DISTINCT buildings.building_id 
            FROM buildings
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
        """Returns a JSON-encoded array of all Tags."""
        return query_json_array(Tags.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Tag whose id is that given."""
        return query_json_item(Tags.sql_query + "WHERE tag_id = %s", (id,))


class Categories:
    sql_query = "SELECT categories.category_id, categories.name AS category_name FROM categories "

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Categories."""
        return query_json_array(Categories.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Category whose id is that given."""
        return query_json_item(Categories.sql_query + "WHERE category_id = %s", (id,))


class Values:
    @staticmethod
    def add(point_name, timestamp, value):
        """Adds a value to the database.

        :param point_name: The point_id of the point from which this value was recorded
        :param timestamp: The UNIX Epoch time when this value was recorded
        :param value: The value that was recorded
        """

        value_type = query_single_cell("""
                    SELECT type
                    FROM value_types
                        INNER JOIN points ON value_types.value_type_id = points.value_type_id
                    WHERE points.name = %s
                    ;""", (point_name,))

        if type(value_type) is float:
                insert("""
            INSERT INTO values (point_id, timestamp, double) VALUES (%s, %s, %s);
            """, (point_name, timestamp, value))
        elif type(value_type) is int or type(value_type) is bool:
            insert("""
            INSERT INTO values (point_id, timestamp, int) VALUES ((SELECT point_id FROM points WHERE name = %s), %s, %s);
            """, (point_name, timestamp, value))
        elif type(value_type) is list:
            insert("""
            INSERT INTO values (point_id, timestamp, int) VALUES ((SELECT point_id FROM points WHERE name = %s), %s, %s);
            """, (point_name, timestamp, value_type.index(value)))
        else:
            raise Exception("value_type.type is of unsupported type")

    @staticmethod
    def get(point_ids, start_time, end_time):
        """Returns JSON-encoded array of values which match the given parameters.

        :param point_ids: A list of the IDs of the points whose values should be included
        :param start_time: The UNIX Epoch time which marks the beginning of the range to be
        included, inclusive
        :param end_time: The UNIX Epoch time which marks the end of the range to be
        included, inclusive
        :return: A JSON-encoded array of Values.
        """
        if len(point_ids) == 0:
            return "[]"
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
