import unittest
from backend.database.Search import Search
from backend.database.models import Buildings


class BuildingSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.buildings("@12"), " buildings.building_id = 12")

    def test_simple_tag(self):
        self.assertEqual(Search.buildings("#1"), " buildings_tags.tag_id = 1")

    def test_simple_room(self):
        with self.assertRaises(Exception): Search.buildings("$12")

    def test_simple_device(self):
        with self.assertRaises(Exception): Search.buildings("%12")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.buildings("*12")

    def test_simple_and(self):
        self.assertEqual(Search.buildings("and"), " AND")

    def test_simple_or(self):
        self.assertEqual(Search.buildings("or"), " OR")

    def test_simple_not(self):
        self.assertEqual(Search.buildings("not"), " NOT")

    def test_simple_floor(self):
        with self.assertRaises(Exception): Search.buildings(":floor = 3")

    def test_simple_type(self):
        with self.assertRaises(Exception): Search.buildings(":type 4")

    def test_simple_unit(self):
        with self.assertRaises(Exception): Search.buildings(":unit 5")

    def test_simple_measurement(self):
        with self.assertRaises(Exception): Search.buildings(":measurement 'temperature'")

    def test_building_room(self):
        with self.assertRaises(Exception): Search.buildings("@3 and $7")

    def test_device_point(self):
        with self.assertRaises(Exception): Search.buildings("%310 or *78")

    def test_building_tag(self):
        self.assertEqual(Search.buildings("@3 and #2"),
                         " buildings.building_id = 3 AND buildings_tags.tag_id = 2")

    # The following tests also test models.py

    def test_ids_where_building(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("@2"))), {2})

    def test_ids_where_building_or_device(self):
        with self.assertRaises(Exception): Buildings.ids_where(Search.buildings("@2 or %4"))

    def test_ids_where_tag(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("#11"))), {1})

    def test_ids_where_building_and_tag(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("@1 and #5"))), {1})

    def test_ids_where_tag_not_building(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("#4 and not @1"))), {2})

    def test_all(self):
        self.assertEqual(Buildings.all(), """[{"building_id":1,"building_name":"CMC","tags":["academic","math_stats","computer_science"]}, 
 {"building_id":2,"building_name":"Evans","tags":["residential"]}, 
 {"building_id":3,"building_name":"Burton","tags":[]}, 
 {"building_id":4,"building_name":"Davis","tags":[]}, 
 {"building_id":5,"building_name":"Boliou","tags":[]}, 
 {"building_id":6,"building_name":"Sayles","tags":[]}]""")

    def test_where_building(self):
        self.assertEqual(Buildings.where(Search.buildings("@2")),
                         """[{"building_id":2,"building_name":"Evans","tags":["residential"]}]""")

    def test_where_building_or_device(self):
        with self.assertRaises(Exception): Buildings.where(Search.buildings("@2 or %4"))

    def test_where_tag(self):
        self.assertEqual(Buildings.where(Search.buildings("#11")),
                         """[{"building_id":1,"building_name":"CMC","tags":["academic","math_stats","computer_science"]}]""")

    def test_where_building_and_tag(self):
        self.assertEqual(Buildings.where(Search.buildings("@1 and #5")),
                         """[{"building_id":1,"building_name":"CMC","tags":["academic","math_stats","computer_science"]}]""")

    def test_where_tag_not_building(self):
        self.assertEqual(Buildings.where(Search.buildings("#4 and not @1")),
                         """[{"building_id":2,"building_name":"Evans","tags":["residential"]}]""")


if __name__ == '__main__':
    unittest.main()
