import re
from backend.database.models import query_single_column


class Search:

    @staticmethod
    def parse(source_string, search_type):
        """Generates a SQL WHERE-clause from the given search source string.

        :param source_string: The source of the search to be parsed
        :param search_type: A string representing the table being searched; one of 'point',
        'device', 'room' or 'building'
        :return: The generated SQL WHERE-clause
        """
        sql_string = " WHERE "

        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        regex = re.compile(
            "([@#$%*]\\d+|and|or|not|:(\\w+) (([<>=]|!=|<=|>=)? ?(\\d+)|(\'\\w+\'))|\\(|\\))")
        # TODO: think harder about the name token
        for token in regex.findall(source_string):
            token = token[0]
            if re.match("@\\d+", token):
                sql_string += " buildings.building_id = " + token[1:]
            elif re.match("#\\d+", token) and search_type == 'point':
                sql_string += " (points_tags.tag_id = " + token[1:] + \
                              " OR devices_tags.tag_id = " + token[1:] + \
                              " OR rooms_tags.tag_id = " + token[1:] + \
                              " OR buildings_tags.tag_id = " + token[1:] + ")"
            elif re.match("#\\d+", token) and search_type == 'device':
                sql_string += " (devices_tags.tag_id = " + token[1:] + \
                              " OR rooms_tags.tag_id = " + token[1:] + \
                              " OR buildings_tags.tag_id = " + token[1:] + ")"
            elif re.match("#\\d+", token) and search_type == 'room':
                sql_string += " (rooms_tags.tag_id = " + token[1:] + \
                              " OR buildings_tags.tag_id = " + token[1:] + ")"
            elif re.match("#\\d+", token) and search_type == 'building':
                sql_string += " buildings_tags.tag_id = " + token[1:]
            elif re.match("\\$\\d+", token):
                sql_string += " rooms.room_id = " + token[1:]
            elif re.match("%\\d+", token):
                sql_string += " devices.device_id = " + token[1:]
            elif re.match("\\*\\d+", token):
                sql_string += " points.point_id = " + token[1:]
            elif re.match(":floor ([<>=]|!=|<=|>=) (\\d+)", token):
                matches = re.match(":floor ([<>=]|!=|<=|>=) (\\d+)", token).groups()
                sql_string += " rooms.floor " + matches[0] + " " + matches[1]
            elif re.match(":type (\\d+)", token):
                matches = re.match(":type (\\d+)", token).groups()
                sql_string += " points.value_type_id = " + matches[0]
            elif re.match(":unit (\\d+)", token):
                matches = re.match(":unit (\\d+)", token).groups()
                sql_string += " value_units.value_unit_id = " + matches[0]
            elif re.match(":measurement (\'\\w+\')", token):
                matches = re.match(":measurement (\'\\w+\')", token).groups()
                sql_string += " value_units.measurement = " + matches[0]
            elif re.match("and", token):
                sql_string += " AND"
            elif re.match("or", token):
                sql_string += " OR"
            elif re.match("not", token):
                sql_string += " NOT"
            elif re.match("\(", token):
                sql_string += "("
            elif re.match("\)", token):
                sql_string += ")"

        return sql_string

    @staticmethod
    def points(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        points.
        """
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        regex = re.compile("^([@#$%*]\\d+|and|or|not|:(floor|type|unit|measurement) (([<>=]|!=|<=|>=)? ?(\\d+)|(\'\\w+\'))|\\(|\\)|\\s+)+$")

        if regex.match(source_string) is None:
            raise Exception("Invalid source string for points.")

        return Search.parse(source_string, 'point')

    @staticmethod
    def devices(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        devices.
        """
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices
        regex = re.compile("^([@#$%]\\d+|and|or|not|:(floor) (([<>=]|!=|<=|>=)? ?(\\d+))|\\(|\\)|\\s+)+$")

        if regex.match(source_string) is None:
            raise Exception("Invalid source string for devices.")

        return Search.parse(source_string, 'device')

    @staticmethod
    def rooms(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        rooms.
        """
        # @ -> buildings, # -> tags, $ -> rooms
        regex = re.compile("^([@#$]\\d+|and|or|not|:(floor) (([<>=]|!=|<=|>=)? ?(\\d+))|\\(|\\)|\\s+)+$")

        if regex.match(source_string) is None:
            raise Exception("Invalid source string for rooms.")

        return Search.parse(source_string, 'room')

    @staticmethod
    def buildings(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        buildings.
        """
        # @ -> buildings, # -> tags
        regex = re.compile("^([@#]\\d+|and|or|not|\\(|\\)|\\s+)+$")

        if regex.match(source_string) is None:
            raise Exception("Invalid source string for buildings.")

        return Search.parse(source_string, 'building')
