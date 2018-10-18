import re

def match_insensitive(pattern, str):
    return re.match(pattern, str, re.IGNORECASE)

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
        regex = re.compile("([@$%*]\\d+|#\\w+|and|or|not|:(\\w+) (([<>=]|!=|<=|>=) (\\d+)|(\"[^\"]+\"))|\\(|\\))")
        # TODO: think harder about the name token
        for token in regex.findall(source_string):
            token = token[0]
            print(type(token))
            print(token)
            if match_insensitive("@\\d+", token):
                sql_string += " buildings.building_id = " + token[1:]
            elif match_insensitive("#\\w+", token):
                sql_string += " tags.name = " + token[1:]
            elif match_insensitive("\\$\\d+", token):
                sql_string += " rooms.room_id = " + token[1:]
            elif match_insensitive("%\\d+", token):
                sql_string += " devices.device_id = " + token[1:]
            elif match_insensitive("\\*\\d+", token):
                sql_string += " points.point_id = " + token[1:]
            elif match_insensitive(":floor ([<>=]|!=|<=|>=) (\\d+)", token):
                matches = match_insensitive(":floor ([<>=]|!=|<=|>=) (\\d+)", token).groups()
                sql_string += " rooms.floor " + matches[0] + " " + matches[1]

            elif match_insensitive("and", token):
                sql_string += " AND"
            elif match_insensitive("or", token):
                sql_string += " OR"
            elif match_insensitive("not", token):
                sql_string += " NOT"
            elif match_insensitive("\(", token):
                sql_string += "("
            elif match_insensitive("\)", token):
                sql_string += ")"

        return sql_string
