import unittest
from backend.database.Search import Search
from backend.database.models import Devices

string_beginning = " WHERE "


class DeviceSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.devices("@12"),
                         string_beginning + " buildings.building_id = 12;")

    def test_simple_tag(self):
        self.assertEqual(Search.devices("#1"),
                         string_beginning + " (devices_tags.tag_id = 1" +
                         " OR rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1);")

    def test_simple_room(self):
        self.assertEqual(Search.devices("$12"),
                         string_beginning + " rooms.room_id = 12;")

    def test_simple_device(self):
        self.assertEqual(Search.devices("%12"),
                         string_beginning + " devices.device_id = 12;")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.devices("*12")

    def test_simple_and(self):
        self.assertEqual(Search.devices("and"),
                         string_beginning + " AND;")

    def test_simple_or(self):
        self.assertEqual(Search.devices("or"),
                         string_beginning + " OR;")

    def test_simple_not(self):
        self.assertEqual(Search.devices("not"),
                         string_beginning + " NOT;")

    def test_simple_floor(self):
        self.assertEqual(Search.devices(":floor = 3"),
                         string_beginning + " rooms.floor = 3;")

    def test_simple_type(self):
        with self.assertRaises(Exception): Search.devices(":type 4")

    def test_simple_unit(self):
        with self.assertRaises(Exception): Search.devices(":unit 5")

    def test_simple_measurement(self):
        with self.assertRaises(Exception): Search.devices(":measurement 'temperature'")

    def test_building_room(self):
        self.assertEquals(Search.devices("@3 and $7"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 7;")

    def test_device_point(self):
        with self.assertRaises(Exception): Search.devices("%310 or *78")

    def test_building_room_device(self):
        self.assertEquals(Search.devices("%6 and @3 and $2"),
                          string_beginning + " devices.device_id = 6 AND buildings.building_id = 3 AND rooms.room_id = 2;")

    def test_parenthesis_building_room_device(self):
        self.assertEquals(Search.devices("(%6 or @3) and $2"),
                          string_beginning + "( devices.device_id = 6 OR buildings.building_id = 3) AND rooms.room_id = 2;")

    def test_nested_parenthesis_building_room_device(self):
        self.assertEquals(Search.devices("%6 or (@3 or $2)"),
                          string_beginning + " devices.device_id = 6 OR( buildings.building_id = 3 OR rooms.room_id = 2);")

    def test_building_floor(self):
        self.assertEquals(Search.devices("@3 and :floor > 2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.floor > 2;")

    def test_search_building(self):
        ids = Devices.ids_where(Search.devices("@2"))
        self.assertEqual(set(ids), {3})

    def test_search_building_floor(self):
        ids = Devices.ids_where(Search.devices("@1 and :floor > 2"))
        self.assertEqual(ids, [2, 1])

    def test_search_building_or_device(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@2 or %4"))), {3, 4})

    def test_search_tag(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("#11"))), {1, 2, 4})

    def test_search_building_and_tag(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@1 and #2"))), set())

    def test_search_tag_not_building(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("#1 and not @2"))), {1})

if __name__ == '__main__':
    unittest.main()
