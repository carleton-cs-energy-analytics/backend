import re
from backend.database.exceptions import InvalidSearchException

# Compiled ahead of time to improve performance.

BUILDINGS_REGEX = re.compile(
    "^("
    "[@#]\\d+|"
    "and|or|not|\\(|\\)|"
    "\\s+"
    ")+$")

ROOMS_REGEX = re.compile(
    "^("
    "[@#$]\\d+|"
    ":(floor) (([<>=] |[<>!]= )?([+-]?[0-9]+))|"
    "and|or|not|\\(|\\)|"
    "\\s+"
    ")+$")

DEVICES_REGEX = re.compile(
    "^("
    "[@#$%]\\d+|"
    ":(floor) (([<>=] |[<>!]= )?([+-]?[0-9]+))|"
    "and|or|not|\\(|\\)|"
    "\\s+"
    ")+$")

POINTS_REGEX = re.compile(
    "^("
    "[@#$%*]\\d+|"
    ":(floor|type|unit|measurement) (([<>=] |[<>!]= )?([+-]?[0-9]+)|\'\\w+\')|"
    "and|or|not|\\(|\\)|\\s+"
    ")+$")

VALUES_REGEX = re.compile(
    "^("
    "~([<>=]|[<>!]=) ?([+-]?([0-9]*[.])?[0-9]+)|"
    "and|or|not|\\(|\\)|\\s+"
    ")+$")

PARSER_REGEX = re.compile(
    "("
    "[@#$%*]\\d+|"
    ":(\\w+) (([<>=] |[<>!]= )?([+-]?[0-9]+)|\'\\w+\')|"
    "~([<>=]|[<>!]=) ?([+-]?([0-9]*[.])?[0-9]+)|"
    "and|or|not|\\(|\\)"
    ")"
)


class Search:
    @staticmethod
    def parse(source_string, search_type):
        """Generates a SQL WHERE-clause from the given search source string.

        :param source_string: The source of the search to be parsed
        :param search_type: A string representing the table being searched; one of 'point',
        'device', 'room' or 'building'
        :return: The generated SQL WHERE-clause
        """
        sql_string = ""

        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points, ~ -> values
        # TODO: think harder about the name token
        for token in PARSER_REGEX.findall(source_string):
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
            elif re.match(":floor ([<>=]|[<>!]=)? ?[+-]?[0-9]+", token):
                matches = re.match(":floor ([<>=]|[<>!]=) ([+-]?[0-9]+)", token).groups()
                if len(matches) == 2:
                    sql_string += " rooms.floor " + matches[0] + " " + matches[1]
                else:
                    sql_string += " rooms.floor = " + matches[1]
            elif re.match(":type \\d+", token):
                matches = re.match(":type (\\d+)", token).groups()
                sql_string += " points.value_type_id = " + matches[0]
            elif re.match(":unit \\d+", token):
                matches = re.match(":unit (\\d+)", token).groups()
                sql_string += " value_units.value_unit_id = " + matches[0]
            elif re.match(":measurement \'\\w+\'", token):
                matches = re.match(":measurement (\'\\w+\')", token).groups()
                sql_string += " value_units.measurement = " + matches[0]
            elif re.match("and", token):
                sql_string += " AND"
            elif re.match("or", token):
                sql_string += " OR"
            elif re.match("not", token):
                sql_string += " NOT"
            elif re.match("\\(", token):
                sql_string += "("
            elif re.match("\\)", token):
                sql_string += ")"
            elif re.match("~([<>=]|[<>!]=) ?([+-]?([0-9]*[.])?[0-9]+)", token):
                sql_string += " (values.double %s OR values.int %s) " % (token[1:], token[1:])

        return sql_string

    @staticmethod
    def points(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        points.
        """
        if source_string is None or len(source_string) == 0:
            return "TRUE"
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        if POINTS_REGEX.match(source_string) is None:
            raise InvalidSearchException("Invalid source string for points: " + source_string)

        return Search.parse(source_string, 'point')

    @staticmethod
    def devices(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        devices.
        """
        if source_string is None or len(source_string) == 0:
            return "TRUE"
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices
        if DEVICES_REGEX.match(source_string) is None:
            raise InvalidSearchException("Invalid source string for devices: " + source_string)

        return Search.parse(source_string, 'device')

    @staticmethod
    def rooms(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        rooms.
        """
        if source_string is None or len(source_string) == 0:
            return "TRUE"
        # @ -> buildings, # -> tags, $ -> rooms
        if ROOMS_REGEX.match(source_string) is None:
            raise InvalidSearchException("Invalid source string for rooms: " + source_string)

        return Search.parse(source_string, 'room')

    @staticmethod
    def buildings(source_string):
        """Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        buildings.
        """
        if source_string is None or len(source_string) == 0:
            return "TRUE"
        # @ -> buildings, # -> tags
        if BUILDINGS_REGEX.match(source_string) is None:
            raise InvalidSearchException("Invalid source string for buildings: " + source_string)

        return Search.parse(source_string, 'building')

    @staticmethod
    def values(source_string):
        """ Uses the given search string to generate a SQL WHERE-clause to be used in a query for
        values.
        """
        if source_string is None or len(source_string) == 0:
            return "TRUE"
        # ~ -> values
        if VALUES_REGEX.match(source_string) is None:
            raise InvalidSearchException("Invalid source string for values: " + source_string)

        return Search.parse(source_string, '')
