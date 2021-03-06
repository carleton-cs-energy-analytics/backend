import unittest
from backend.database.Search import Search
from backend.database.models import Devices


class DeviceSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.devices("@12"), " buildings.building_id = 12")

    def test_simple_tag(self):
        self.assertEqual(Search.devices("#1"), " (devices_tags.tag_id = 1" +
                         " OR rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1)")

    def test_simple_room(self):
        self.assertEqual(Search.devices("$12"), " rooms.room_id = 12")

    def test_simple_device(self):
        self.assertEqual(Search.devices("%12"), " devices.device_id = 12")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.devices("*12")

    def test_simple_and(self):
        self.assertEqual(Search.devices("and"), " AND")

    def test_simple_or(self):
        self.assertEqual(Search.devices("or"), " OR")

    def test_simple_not(self):
        self.assertEqual(Search.devices("not"), " NOT")

    def test_simple_floor(self):
        self.assertEqual(Search.devices(":floor = 3"), " rooms.floor = 3")

    def test_simple_type(self):
        with self.assertRaises(Exception): Search.devices(":type 4")

    def test_simple_unit(self):
        with self.assertRaises(Exception): Search.devices(":unit 5")

    def test_simple_measurement(self):
        with self.assertRaises(Exception): Search.devices(":measurement 'temperature'")

    def test_building_room(self):
        self.assertEqual(Search.devices("@3 and $7"),
                         " buildings.building_id = 3 AND rooms.room_id = 7")

    def test_device_point(self):
        with self.assertRaises(Exception): Search.devices("%310 or *78")

    def test_building_room_device(self):
        self.assertEqual(Search.devices("%6 and @3 and $2"),
                         " devices.device_id = 6 AND buildings.building_id = 3 AND rooms.room_id = 2")

    def test_parenthesis_building_room_device(self):
        self.assertEqual(Search.devices("(%6 or @3) and $2"),
                         "( devices.device_id = 6 OR buildings.building_id = 3) AND rooms.room_id = 2")

    def test_nested_parenthesis_building_room_device(self):
        self.assertEqual(Search.devices("%6 or (@3 or $2)"),
                         " devices.device_id = 6 OR( buildings.building_id = 3 OR rooms.room_id = 2)")

    def test_building_floor(self):
        self.assertEqual(Search.devices("@3 and :floor > 2"),
                         " buildings.building_id = 3 AND rooms.floor > 2")

    # The following tests also test models.py

    def test_ids_where_building(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@2"))), {3})

    def test_ids_where_building_floor(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@1 and :floor > 2"))), {1, 2})

    def test_ids_where_building_or_device(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@2 or %4"))), {3, 4})

    def test_ids_where_tag(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("#11"))), {1, 2, 4})

    def test_ids_where_building_and_tag(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("@1 and #2"))), set())

    def test_ids_where_tag_not_building(self):
        self.assertEqual(set(Devices.ids_where(Search.devices("#1 and not @2"))), {1})

    def test_all(self):
        self.assertEqual(Devices.all(), """[{"device_id":2,"device_name":"Fishbowl vav","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","computer_science"],"description":null}, 
 {"device_id":1,"device_name":"Fishbowl thermostat","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","thermostat","computer_science"],"description":null}, 
 {"device_id":4,"device_name":"102 Lab thermostat","room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","tags":["math_stats","academic","computer_science"],"description":null}, 
 {"device_id":3,"device_name":"Thermostat in Evans 107","room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","tags":["thermostat","residential","single","residence"],"description":null}]""")

    def test_where_building(self):
        self.assertEqual(Devices.where(Search.devices("@2")),
                         '[{"device_id":3,"device_name":"Thermostat in Evans 107","room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","tags":["thermostat","residential","single","residence"],"description":null}]')

    def test_where_building_floor(self):
        self.assertEqual(Devices.where(Search.devices("@1 and :floor > 2")), """[{"device_id":1,"device_name":"Fishbowl thermostat","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","thermostat","computer_science"],"description":null}, 
 {"device_id":2,"device_name":"Fishbowl vav","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","computer_science"],"description":null}]""")

    def test_where_building_or_device(self):
        self.assertEqual(Devices.where(Search.devices("@2 or %4")), """[{"device_id":3,"device_name":"Thermostat in Evans 107","room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","tags":["thermostat","residential","single","residence"],"description":null}, 
 {"device_id":4,"device_name":"102 Lab thermostat","room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","tags":["math_stats","academic","computer_science"],"description":null}]""")

    def test_where_tag(self):
        self.assertEqual(Devices.where(Search.devices("#11")), """[{"device_id":2,"device_name":"Fishbowl vav","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","computer_science"],"description":null}, 
 {"device_id":1,"device_name":"Fishbowl thermostat","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","thermostat","computer_science"],"description":null}, 
 {"device_id":4,"device_name":"102 Lab thermostat","room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","tags":["math_stats","academic","computer_science"],"description":null}]""")

    def test_where_building_and_tag(self):
        self.assertEqual(Devices.where(Search.devices("@1 and #2")), "[]")

    def test_where_tag_not_building(self):
        self.assertEqual(Devices.where(Search.devices("#1 and not @2")),
                         """[{"device_id":1,"device_name":"Fishbowl thermostat","room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","tags":["classroom","math_stats","academic","thermostat","computer_science"],"description":null}]""")


if __name__ == '__main__':
    unittest.main()
