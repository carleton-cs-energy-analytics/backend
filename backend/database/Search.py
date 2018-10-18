import re

class Search:

    def __init__(self, source_string):
        self.source_string = source_string
        self.results = None

    @staticmethod
    def parse(source_string):
        sql_string = """
            SELECT points.point_id FROM points
            LEFT JOIN points_tags pt ON points.point_id = pt.point_id
            WHERE
        """

        # @ -> buildings, # -> tags, $ -> rooms, % -> devices, * -> points
        regex = re.compile("([@$%*]\\d+|#\\w+|and|or|not|:(\\w+) (([<>=]|!=|<=|>=) (\\d+)|(\'\\w+\'))|\\(|\\))")
        # TODO: think harder about the name token
        for token in regex.findall(source_string):
            token = token[0]
            print(type(token))
            print(token)
            if re.match("@\\d+", token):
                sql_string += " buildings.building_id = " + token[1:]
            elif re.match("#\\w+", token):
                sql_string += " tags.name = " + token[1:]
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
                sql_string += " value_types.value_type_id = " + matches[0]
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
