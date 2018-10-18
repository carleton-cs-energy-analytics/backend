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
                         string_beginning + "buildings.building_id = 12")

    def test_simple_room(self):
        self.assertEqual(Search.parse("$12"),
                         string_beginning + "rooms.room_id = 12")

    def test_simple_device(self):
        self.assertEqual(Search.parse("%12"),
                         string_beginning + "devices.device_id = 12")

    def test_simple_point(self):
        self.assertEqual(Search.parse("*12"),
                         string_beginning + "points.point_id = 12")

    # def test_simple_floor(self):
