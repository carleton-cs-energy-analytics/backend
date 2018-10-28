import re
from backend.database.models import query_single_column


class Search:

    @staticmethod
    def parse(source_string):
        sql_string = " WHERE "

        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        regex = re.compile(
            "([@#$%*]\\d+|and|or|not|:(\\w+) (([<>=]|!=|<=|>=)? ?(\\d+)|(\'\\w+\'))|\\(|\\))")
        # TODO: think harder about the name token
        for token in regex.findall(source_string):
            token = token[0]
            if re.match("@\\d+", token):
                sql_string += " buildings.building_id = " + token[1:]
            elif re.match("#\\d+", token):
                sql_string += " (points_tags.tag_id = " + token[1:] + \
                              " OR devices_tags.tag_id = " + token[1:] + \
                              " OR rooms_tags.tag_id = " + token[1:] + \
                              " OR buildings_tags.tag_id = " + token[1:] + ")"
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

        return sql_string + ";"

    @staticmethod
    def points(source_string):
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        regex = "^([@#$%*]\\d+|and|or|not|:(floor|type|unit|measurement) (([<>=]|!=|<=|>=)? ?(\\d+)|(\'\\w+\'))|\\(|\\))+$"

        if re.match(regex, source_string) is None:
            raise Exception("Invalid source string for points.")

        return Search.parse(source_string)

    @staticmethod
    def devices(source_string):
        # @ -> buildings, # -> tags, $ -> rooms, % -> devices
        regex = "^([@#$%]\\d+|and|or|not|:(floor) (([<>=]|!=|<=|>=)? ?(\\d+))|\\(|\\))+$"

        if re.match(regex, source_string) is None:
            raise Exception("Invalid source string for devices.")

        return Search.parse(source_string)

    @staticmethod
    def rooms(source_string):
        # @ -> buildings, # -> tags, $ -> rooms
        regex = "^([@#$]\\d+|and|or|not|:(floor) (([<>=]|!=|<=|>=)? ?(\\d+))|\\(|\\))+$"

        if re.match(regex, source_string) is None:
            raise Exception("Invalid source string for rooms.")

        return Search.parse(source_string)

    @staticmethod
    def buildings(source_string):
        # @ -> buildings, # -> tags
        regex = "^([@#]\\d+|and|or|not (([<>=]|!=|<=|>=)? ?(\\d+))|\\(|\\))+$"

        if re.match(regex, source_string) is None:
            raise Exception("Invalid source string for buildings.")

        return Search.parse(source_string)
