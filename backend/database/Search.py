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
        regex = re.compile("")
        # TODO: think harder about the name token
        for token in regex.findall(source_string):
            if re.compile("@\\d+").match(token):
                # add to the sql string



