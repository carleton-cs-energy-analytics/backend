import unittest
from backend.database.Search import Search

string_beginning = """
            SELECT points.point_id FROM points
            LEFT JOIN points_tags pt ON points.point_id = pt.point_id
            WHERE
        """


class SearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.parse("@12"),
                         string_beginning + " buildings.building_id = 12")

    def test_simple_room(self):
        self.assertEqual(Search.parse("$12"),
                         string_beginning + " rooms.room_id = 12")

    def test_simple_device(self):
        self.assertEqual(Search.parse("%12"),
                         string_beginning + " devices.device_id = 12")

    def test_simple_point(self):
        self.assertEqual(Search.parse("*12"),
                         string_beginning + " points.point_id = 12")

    def test_simple_and(self):
        self.assertEqual(Search.parse("and"),
                         string_beginning + " AND")

    def test_simple_or(self):
        self.assertEqual(Search.parse("or"),
                         string_beginning + " OR")

    def test_simple_not(self):
        self.assertEqual(Search.parse("not"),
                         string_beginning + " NOT")

    # def test_simple_floor(self):

    def test_building_room(self):
        self.assertEquals(Search.parse("@3 and $7"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 7")

    def test_device_point(self):
        self.assertEquals(Search.parse("%310 or *78"),
                          string_beginning + " devices.device_id = 310 OR points.point_id = 78")

    def test_building_room_device_point(self):
        self.assertEquals(Search.parse("*1 and %6 and @3 and $2"),
                          string_beginning + " points.point_id = 1 AND devices.device_id = 6 AND buildings.building_id = 3 AND rooms.room_id = 2")

    def test_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.parse("*1 and (%6 or @3) and $2"),
                          string_beginning + " points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3) AND rooms.room_id = 2")

    def test_nested_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.parse("(*1 and (%6 or @3)) or $2"),
                          string_beginning + "( points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3)) OR rooms.room_id = 2")

    def test_building_floor(self):
        self.assertEquals(Search.parse("@3 and :floor > 2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.floor > 2")


if __name__ == '__main__':
    unittest.main()