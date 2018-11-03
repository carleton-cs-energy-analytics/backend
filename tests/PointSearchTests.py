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

    def test_all(self):
        self.assertEqual(Points.all(), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":1,"point_name":"CMC.328.RT","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","get","room_temp"],"description":"Room Temp in CMC 328"}, 
 {"point_id":5,"point_name":"CMC.102.SP","device_id":4,"device_name":null,"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["math_stats","academic","computer_science","set"],"description":"Thermostat Set Point in CMC 102"}, 
 {"point_id":4,"point_name":"EV.RM107.SP","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":3,"storage_kind":"double","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","single","residence","room_temp","set"],"description":"Thermostat Set Point in Evans 107"}, 
 {"point_id":3,"point_name":"EV.RM107.RT","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","get","single","residence","room_temp"],"description":"Room Temp in Evans 107"}]""")

    def test_get_by_id(self):
        self.assertEqual(Points.get_by_id(1), """{"point_id":1,"point_name":"CMC.328.RT","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","get","room_temp"],"description":"Room Temp in CMC 328"}""")

    def test_get_by_ids(self):
        self.assertEqual(Points.get_by_ids([2,4,6]), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":4,"point_name":"EV.RM107.SP","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":3,"storage_kind":"double","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","single","residence","room_temp","set"],"description":"Thermostat Set Point in Evans 107"}]""")

    def test_where_building(self):
        self.assertEqual(Points.where(Search.points("@2")), """[{"point_id":4,"point_name":"EV.RM107.SP","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":3,"storage_kind":"double","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","single","residence","room_temp","set"],"description":"Thermostat Set Point in Evans 107"}, 
 {"point_id":3,"point_name":"EV.RM107.RT","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","get","single","residence","room_temp"],"description":"Room Temp in Evans 107"}]""")

    def test_where_building_floor(self):
        self.assertEqual(Points.where(Search.points("@1 and :floor > 2")), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":1,"point_name":"CMC.328.RT","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","get","room_temp"],"description":"Room Temp in CMC 328"}]""")

    def test_where_building_or_device(self):
        self.assertEqual(Points.where(Search.points("@2 or %4")), """[{"point_id":4,"point_name":"EV.RM107.SP","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":3,"storage_kind":"double","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","single","residence","room_temp","set"],"description":"Thermostat Set Point in Evans 107"}, 
 {"point_id":3,"point_name":"EV.RM107.RT","device_id":3,"device_name":null,"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["thermostat","residential","get","single","residence","room_temp"],"description":"Room Temp in Evans 107"}, 
 {"point_id":5,"point_name":"CMC.102.SP","device_id":4,"device_name":null,"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["math_stats","academic","computer_science","set"],"description":"Thermostat Set Point in CMC 102"}]""")

    def test_where_tag(self):
        self.assertEqual(Points.where(Search.points("#11")), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":1,"point_name":"CMC.328.RT","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","get","room_temp"],"description":"Room Temp in CMC 328"}, 
 {"point_id":5,"point_name":"CMC.102.SP","device_id":4,"device_name":null,"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["math_stats","academic","computer_science","set"],"description":"Thermostat Set Point in CMC 102"}]""")

    def test_where_building_and_tag(self):
        self.assertEqual(Points.where(Search.points("@1 and #2")), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":5,"point_name":"CMC.102.SP","device_id":4,"device_name":null,"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["math_stats","academic","computer_science","set"],"description":"Thermostat Set Point in CMC 102"}]""")

    def test_where_tag_not_building(self):
        self.assertEqual(Points.where(Search.points("#2 and not @2")), """[{"point_id":2,"point_name":"CMC.328.SP","device_id":1,"device_name":null,"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["classroom","math_stats","academic","thermostat","computer_science","room_temp","set"],"description":"Thermostat Set Point in CMC 328"}, 
 {"point_id":5,"point_name":"CMC.102.SP","device_id":4,"device_name":null,"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","value_type":{"value_type_id":2,"storage_kind":"int","cases":null},"value_unit":{"value_unit_id":1,"measurement":"temperature","unit":"fahrenheit"},"tags":["math_stats","academic","computer_science","set"],"description":"Thermostat Set Point in CMC 102"}]""")

    def test_is_double_false(self):
        self.assertEqual(Points.value_is_double(1), False)

    def test_is_double_true(self):
        self.assertEqual(Points.value_is_double(4), True)

if __name__ == '__main__':
    unittest.main()
