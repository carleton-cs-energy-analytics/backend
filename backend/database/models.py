import os
import sys
import psycopg2

CONN = psycopg2.connect(host=os.environ.get('DATABASE_HOST') or '',
                        dbname=os.environ.get('DATABASE_NAME') or 'energy-dev',
                        user=os.environ.get('DATABASE_USER') or '',
                        password=os.environ.get('DATABASE_PASSWORD') or '')
CONN.autocommit = True


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
    return query_single_cell("SELECT json_agg(a)::TEXT FROM (" + query + ") AS a;", vars)


def query_json_item(query, vars=None):
    """Returns a JSON-encoded string of the single result of the given SQL query.

    The query is wrapped a PostgreSQL `row_to_json` function, the database query is issued, and then
    the results of the query are unwrapped to get the JSON-encoded string itself.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: A string containing the JSON-encoded result of the query
    """
    return query_single_cell("SELECT row_to_json(a)::TEXT FROM (" + query + ") AS a;", vars)


def query_json_single_column(query, vars=None):
    """Returns a JSON-encoded string of the values in the column aliased `col` from the given query.

    :param query: The SQL query
    :param vars: Any values that need to be injected into the SQL query
    :return: A string containing the JSON-encoded result of the query
    """
    return query_single_cell("SELECT json_agg(col)::TEXT FROM (" + query + ") AS a;", vars)


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


def insert_values(query, items):
    """Used for inserting values into the database. Takes a query and a list of 3-tuples, appends
    the 3-tuples to the query, and then executes and commits it.

    :param query: The SQL query
    :param items: A list of 3-tuples to be appended to the end of the query
    """
    with CONN.cursor() as curs:
        # sanitizes (mogrify) the items, creating strings, and then joins them together with commas
        args_str = ','.join(curs.mogrify("(%s, %s, %s)", item).decode("utf-8") for item in items)
        curs.execute(query + args_str + ";")
        CONN.commit()


def execute_and_commit(query, vars):
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
        WHERE %s
        ORDER BY points.name
        """

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Points."""
        return query_json_array(Points.sql_query % "TRUE")

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Point whose id is that given."""
        return query_json_item(Points.sql_query % "point_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Points whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Points.sql_query % "point_id IN %s", (tuple(ids),))

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
        return query_single_column(base_query + " WHERE (" + where_clause + ")")

    @staticmethod
    def counts_where(where_clause):
        """Returns a list of the ids of all Points which match the given WHERE-clause."""
        base_query = """
            SELECT points.value_type_id, COUNT(DISTINCT points.point_id)
            FROM points
                   LEFT JOIN devices ON points.device_id = devices.device_id
                   LEFT JOIN rooms ON devices.room_id = rooms.room_id
                   LEFT JOIN buildings ON rooms.building_id = buildings.building_id
                   LEFT JOIN value_units ON points.value_unit_id = value_units.value_unit_id
                   LEFT JOIN points_tags ON points.point_id = points_tags.point_id
                   LEFT JOIN devices_tags ON devices.device_id = devices_tags.device_id
                   LEFT JOIN rooms_tags ON rooms.room_id = rooms_tags.room_id
                   LEFT JOIN buildings_tags ON buildings.building_id = buildings_tags.building_id
            WHERE (%s)
            GROUP BY points.value_type_id
            """
        return query_json_array(base_query % where_clause)


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

        return query_single_column(base_query + " WHERE (" + where_clause + ")")


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
        WHERE %s
        ORDER BY rooms.name
        """

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Rooms."""
        return query_json_array(Rooms.sql_query % "TRUE")

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Room whose id is that given."""
        return query_json_item(Rooms.sql_query % "room_id = %s", (id,))

    @staticmethod
    def get_by_ids(ids):
        """Returns a JSON-encoded array of all Rooms whose ids were given."""
        if len(ids) == 0:
            return "[]"
        return query_json_array(Rooms.sql_query % "room_id IN %s", (tuple(ids),))

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

        return query_single_column(base_query + " WHERE (" + where_clause + ")")


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

        return query_single_column(base_query + " WHERE (" + where_clause + ")")

    @staticmethod
    def floors(building_id):
        return query_json_single_column(
            "SELECT DISTINCT floor AS col FROM rooms WHERE building_id = %s ORDER BY floor",
            building_id)

    @staticmethod
    def all_floors():
        return query_json_single_column("SELECT DISTINCT floor AS col FROM rooms ORDER BY floor")


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


class Units:
    sql_query = "SELECT value_unit_id AS unit_id, unit AS unit_name, measurement FROM value_units "

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Categories."""
        return query_json_array(Units.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Category whose id is that given."""
        return query_json_item(Units.sql_query + "WHERE value_unit_id = %s", (id,))

    @staticmethod
    def get_all_measurements():
        return query_json_single_column("SELECT DISTINCT measurement AS col FROM value_units")


class Types:
    sql_query = "SELECT value_type_id AS type_id, name AS type_name, type AS cases " \
                "FROM value_types "

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Categories."""
        return query_json_array(Types.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Category whose id is that given."""
        return query_json_item(Types.sql_query + "WHERE category_id = %s", (id,))


class Values:
    @staticmethod
    def _get_id_and_type(point_name):
        """Gets the point id and value type for a given point name.

        :param point_name: The point name
        :return: A tuple with the point id and value type for the point name or None if the point
        does not exist in the database.
        """
        return query_single_row("""
                            SELECT point_id, type
                            FROM value_types
                                INNER JOIN points ON value_types.value_type_id = points.value_type_id
                            WHERE points.name = %s
                            ;""", (point_name,))

    @staticmethod
    def _prepare_add(values):
        """Transforms value data in preparation for being added to the database. Takes a list of
        tuples containing the point name, the timestamp, and the value as it appears in Siemens
        reports, and outputs two lists, with tuples containing the point id, the timestamp, and the
        value in the form in which it goes into the database.

        :param values: A list of 3-tuples in the form `(point_name, timestamp, value)` where values
        are ints, doubles, or enum strings.
        :return: Two lists where the first one is a list of 3-tuples where the values to be inserted
        into the database are ints and another one for doubles. The first value is now point ids
        rather than names.
        """
        point_info = {}
        int_values = []
        float_values = []
        for (point_name, timestamp, value) in values:
            # Only want to get the point id and value type once for each point name
            if point_name not in point_info:
                point_info[point_name] = Values._get_id_and_type(point_name)
                if point_info[point_name] is None:
                    print("The point", point_name, "doesn't exist", file=sys.stderr)
                    # This line is here, rather than 4 lines down to avoid repeat printouts
                    # TODO: Consider throwing an error instead.

            # Don't want to add values where the point is not in the database
            if point_info[point_name] is None:
                continue

            (point_id, value_type) = point_info[point_name]

            # Appends the transformed 3-tuple to the relevant list
            if type(value_type) is float:
                float_values.append((point_id, timestamp, value))
            elif type(value_type) is int or type(value_type) is bool:
                int_values.append((point_id, timestamp, value))
            elif type(value_type) is list:
                int_values.append((point_id, timestamp, value_type.index(value)))
            else:
                raise Exception("value_type.type is of unsupported type")

        return int_values, float_values

    @staticmethod
    def add(values):
        """Adds a list of values to the database.

        :param values: A list of 3-tuples in the form `(point_name, timestamp, value)` where values
        are ints, doubles, or enum strings.
        """

        int_values, float_values = Values._prepare_add(values)

        # Only want to insert values if there are values to be inserted for the particular type
        if len(float_values) > 0:
            insert_values("""
                INSERT INTO values (point_id, timestamp, double) VALUES 
                """, float_values)

        if len(int_values) > 0:
            insert_values("""
                INSERT INTO values (point_id, timestamp, int) VALUES 
                """, int_values)

    @staticmethod
    def get(point_ids, start_time, end_time, where_clause='TRUE'):
        """Returns JSON-encoded array of values which match the given parameters.

        :param point_ids: A list of the IDs of the points whose values should be included
        :param start_time: The UNIX Epoch time which marks the beginning of the range to be
        included, inclusive
        :param end_time: The UNIX Epoch time which marks the end of the range to be
        included, inclusive
        :param where_clause: Additional restrictions to add to the WHERE clause
        :return: A JSON-encoded array of Values.
        """
        if len(point_ids) == 0:
            return "[]"
        return query_json_array("""
            SELECT value_id, 
                points.name AS point_name, 
                timestamp, 
                '[false,true]'::JSONB->int::INT AS value,
                (""" + where_clause + """) AS matches
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
                   LEFT JOIN value_types ON points.value_type_id = value_types.value_type_id
            WHERE int IS NOT NULL
              AND points.value_type_id = 1
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            UNION ALL
            SELECT value_id, 
                points.name AS point_name, 
                timestamp, 
                to_jsonb(int) AS value,
                (""" + where_clause + """) AS matches
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
                   LEFT JOIN value_types ON points.value_type_id = value_types.value_type_id
            WHERE int IS NOT NULL
              AND points.value_type_id = 2
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            UNION ALL
            SELECT value_id, 
                points.name AS point_name, 
                timestamp, 
                (type->values.int::INT) AS value,
                (""" + where_clause + """) AS matches
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
                   LEFT JOIN value_types ON points.value_type_id = value_types.value_type_id
            WHERE int IS NOT NULL
              AND points.value_type_id > 3
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            UNION ALL
            SELECT value_id, 
                points.name AS point_name, 
                timestamp, 
                to_jsonb(double) AS value,
                (""" + where_clause + """) AS matches
            FROM values
                   LEFT JOIN points ON values.point_id = points.point_id
            WHERE double IS NOT NULL
              AND values.point_id IN %s
              AND %s <= timestamp
              AND timestamp <= %s
            """, (
            tuple(point_ids), start_time, end_time,
            tuple(point_ids), start_time, end_time,
            tuple(point_ids), start_time, end_time,
            tuple(point_ids), start_time, end_time,
        ))

    @staticmethod
    def get_count(point_ids, start_time, end_time, where_clause='TRUE'):
        """Returns JSON-encoded array of values which match the given parameters.

        :param point_ids: A list of the IDs of the points whose values should be included
        :param start_time: The UNIX Epoch time which marks the beginning of the range to be
        included, inclusive
        :param end_time: The UNIX Epoch time which marks the end of the range to be
        included, inclusive
        :param where_clause: Additional restrictions to add to the WHERE clause
        :return: A JSON-encoded array of Values.
        """
        if len(point_ids) == 0:
            return "[]"
        return query_single_cell("""
                SELECT COUNT(value_id)
                FROM values
                       LEFT JOIN points ON values.point_id = points.point_id
                WHERE values.point_id IN %s
                  AND %s <= timestamp
                  AND timestamp <= %s
                  AND (""" + where_clause + """)
                """, (tuple(point_ids), start_time, end_time,))

    @staticmethod
    def has_any_since(time):
        return query_single_cell("SELECT exists(SELECT 1 FROM values WHERE timestamp>=%s)", (time,))

    @staticmethod
    def most_recent_timestamp():
        return query_single_cell("SELECT max(timestamp) FROM values")


class Rules:
    sql_query = "SELECT rule_id, name AS rule_name, priority, url, point_search, value_search " \
                "FROM rules "

    @staticmethod
    def all():
        """Returns a JSON-encoded array of all Rules."""
        return query_json_array(Rules.sql_query)

    @staticmethod
    def get_by_id(id):
        """Returns the JSON-encoded Rule whose id is that given."""
        return query_json_item(Rules.sql_query + "WHERE rule_id = %s", (id,))

    @staticmethod
    def searches(id):
        return query_single_row("SELECT point_search, value_search FROM rules "
                                "WHERE rule_id = %s", (id,))

    @staticmethod
    def add(name, url, point_search, value_search):
        """Adds a new rule to the database."""
        execute_and_commit("INSERT INTO rules (name, url, point_search, value_search) "
                           "VALUES (%s, %s, %s, %s)", (name, url, point_search, value_search))

    @staticmethod
    def delete(id):
        """Deletes a rule from the database."""
        execute_and_commit("DELETE FROM rules WHERE rule_id = %s", (id,))

    @staticmethod
    def rename(id, name):
        """Renames an existing rule."""
        execute_and_commit("UPDATE rules SET name = %s WHERE rule_id = %s", (name, id))
        return query_single_cell("SELECT name FROM rules WHERE rule_id = %s", (id,))
