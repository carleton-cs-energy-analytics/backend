import unittest
from backend.database.Search import Search
from backend.database.models import Points

string_beginning = " WHERE "


class PointSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.points("@12"),
                         string_beginning + " buildings.building_id = 12")

    def test_simple_tag(self):
        self.assertEqual(Search.points("#1"),
                         string_beginning + " (points_tags.tag_id = 1 OR devices_tags.tag_id = 1" +
                         " OR rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1)")

    def test_simple_room(self):
        self.assertEqual(Search.points("$12"),
                         string_beginning + " rooms.room_id = 12")

    def test_simple_device(self):
        self.assertEqual(Search.points("%12"),
                         string_beginning + " devices.device_id = 12")

    def test_simple_point(self):
        self.assertEqual(Search.points("*12"),
                         string_beginning + " points.point_id = 12")

    def test_simple_and(self):
        self.assertEqual(Search.points("and"),
                         string_beginning + " AND")

    def test_simple_or(self):
        self.assertEqual(Search.points("or"),
                         string_beginning + " OR")

    def test_simple_not(self):
        self.assertEqual(Search.points("not"),
                         string_beginning + " NOT")

    def test_simple_floor(self):
        self.assertEqual(Search.points(":floor = 3"),
                         string_beginning + " rooms.floor = 3")

    def test_simple_type(self):
        self.assertEqual(Search.points(":type 4"),
                         string_beginning + " points.value_type_id = 4")

    def test_simple_unit(self):
        self.assertEqual(Search.points(":unit 5"),
                         string_beginning + " value_units.value_unit_id = 5")

    def test_simple_measurement(self):
        self.assertEqual(Search.points(":measurement 'temperature'"),
                         string_beginning + " value_units.measurement = 'temperature'")

    def test_building_room(self):
        self.assertEquals(Search.points("@3 and $7"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 7")

    def test_device_point(self):
        self.assertEquals(Search.points("%310 or *78"),
                          string_beginning + " devices.device_id = 310 OR points.point_id = 78")

    def test_building_room_device_point(self):
        self.assertEquals(Search.points("*1 and %6 and @3 and $2"),
                          string_beginning + " points.point_id = 1 AND devices.device_id = 6 AND buildings.building_id = 3 AND rooms.room_id = 2")

    def test_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.points("*1 and (%6 or @3) and $2"),
                          string_beginning + " points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3) AND rooms.room_id = 2")

    def test_nested_parenthesis_building_room_device_point(self):
        self.assertEquals(Search.points("(*1 and (%6 or @3)) or $2"),
                          string_beginning + "( points.point_id = 1 AND( devices.device_id = 6 OR buildings.building_id = 3)) OR rooms.room_id = 2")

    def test_building_floor(self):
        self.assertEquals(Search.points("@3 and :floor > 2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.floor > 2")

    # The following tests also test models.py

    def test_ids_where_building(self):
        self.assertEqual(set(Points.ids_where(Search.points("@2"))), {3, 4})

    def test_ids_where_building_floor(self):
        self.assertEqual(set(Points.ids_where(Search.points("@1 and :floor > 2"))), {1, 2})

    def test_ids_where_building_or_device(self):
        self.assertEqual(set(Points.ids_where(Search.points("@2 or %4"))), {3, 4, 5})

    def test_ids_where_tag(self):
        self.assertEqual(set(Points.ids_where(Search.points("#11"))), {1, 2, 5})

    def test_ids_where_building_and_tag(self):
        self.assertEqual(set(Points.ids_where(Search.points("@1 and #2"))), {2, 5})

    def test_ids_where_tag_not_building(self):
        self.assertEqual(set(Points.ids_where(Search.points("#2 and not @2"))), {2, 5})

if __name__ == '__main__':
    unittest.main()
