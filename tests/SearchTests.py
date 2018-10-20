import unittest
from backend.database.Search import Search

string_beginning = """
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
        WHERE
        """


class SearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.parse("@12"),
                         string_beginning + " buildings.building_id = 12;")

    def test_simple_tag(self):
        self.assertEqual(Search.parse("#1"),
                         string_beginning + " (points_tags.tag_id = 1 OR devices_tags.tag_id = 1" +
                         " OR rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1);")

    def test_simple_room(self):
        self.assertEqual(Search.parse("$12"),
                         string_beginning + " rooms.room_id = 12;")

    def test_simple_device(self):
        self.assertEqual(Search.parse("%12"),
                         string_beginning + " devices.device_id = 12;")

    def test_simple_point(self):
        self.assertEqual(Search.parse("*12"),
                         string_beginning + " points.point_id = 12;")

    def test_simple_and(self):
        self.assertEqual(Search.parse("and"),
                         string_beginning + " AND;")

    def test_simple_or(self):
        self.assertEqual(Search.parse("or"),
                         string_beginning + " OR;")

    def test_simple_not(self):
        self.assertEqual(Search.parse("not"),
                         string_beginning + " NOT;")

    def test_simple_floor(self):
        self.assertEqual(Search.parse(":floor = 3"),
                         string_beginning + " rooms.floor = 3;")

    def test_simple_type(self):
        self.assertEqual(Search.parse(":type 4"),
                         string_beginning + " points.value_type_id = 4;")

    def test_simple_unit(self):
        self.assertEqual(Search.parse(":unit 5"),
                         string_beginning + " value_units.value_unit_id = 5;")

    def test_simple_measurement(self):
        self.assertEqual(Search.parse(":measurement 'temperature'"),
                         string_beginning + " value_units.measurement = 'temperature';")

    def test_building_room(self):
        self.assertEquals(Search.parse("@3 and $7"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 7;")

    def test_device_point(self):
        self.assertEquals(Search.parse("%310 or *78"),
                          string_beginning + " devices.device_id = 310 OR points.point_id = 78;")

    def test_building_room_device_point(self):
        self.assertEquals(Search.parse("*1 and %6 and @3 and $2"),
                          string_beginning + " points.point_id = 1 AND devices.device_id = 6 AND buildings.building_id = 3 AND rooms.room_id = 2;")

    def test_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.parse("*1 and (%6 or @3) and $2"),
                          string_beginning + " points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3) AND rooms.room_id = 2;")

    def test_nested_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.parse("(*1 and (%6 or @3)) or $2"),
                          string_beginning + "( points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3)) OR rooms.room_id = 2;")

    def test_building_floor(self):
        self.assertEquals(Search.parse("@3 and :floor > 2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.floor > 2;")

    def test_search_building(self):
        search = Search("@2")
        self.assertEqual(set(search.get_ids()), {3, 4})

    def test_search_building_floor(self):
        search = Search("@1 and :floor > 2")
        self.assertEqual(search.get_ids(), [2, 1])

    def test_search_building_or_room(self):
        self.assertEqual(set(Search("@2 or %4").get_ids()), {3, 4, 5})

    def test_search_tag(self):
        self.assertEqual(set(Search("#11").get_ids()), {1, 2, 5})

    def test_search_building_and_tag(self):
        self.assertEqual(set(Search("@1 and #2").get_ids()), {2, 5})

    def test_search_tag_not_building(self):
        self.assertEqual(set(Search("#2 and not @2").get_ids()), {2, 5})

if __name__ == '__main__':
    unittest.main()
