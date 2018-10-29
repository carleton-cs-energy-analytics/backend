import unittest
from backend.database.Search import Search
from backend.database.models import Buildings

string_beginning = " WHERE "


class BuildingSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.buildings("@12"),
                         string_beginning + " buildings.building_id = 12;")

    def test_simple_tag(self):
        self.assertEqual(Search.buildings("#1"),
                         string_beginning + " buildings_tags.tag_id = 1;")

    def test_simple_room(self):
        with self.assertRaises(Exception): Search.buildings("$12")

    def test_simple_device(self):
        with self.assertRaises(Exception): Search.buildings("%12")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.buildings("*12")

    def test_simple_and(self):
        self.assertEqual(Search.buildings("and"),
                         string_beginning + " AND;")

    def test_simple_or(self):
        self.assertEqual(Search.buildings("or"),
                         string_beginning + " OR;")

    def test_simple_not(self):
        self.assertEqual(Search.buildings("not"),
                         string_beginning + " NOT;")

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
        self.assertEquals(Search.buildings("@3 and #2"),
                          string_beginning + " buildings.building_id = 3 AND buildings_tags.tag_id = 2;")

    def test_search_building(self):
        ids = Buildings.ids_where(Search.buildings("@2"))
        self.assertEqual(set(ids), {2})

    def test_search_building_or_device(self):
        with self.assertRaises(Exception): Buildings.ids_where(Search.buildings("@2 or %4"))

    def test_search_tag(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("#11"))), {1})

    def test_search_building_and_tag(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("@1 and #5"))), {1})

    def test_search_tag_not_building(self):
        self.assertEqual(set(Buildings.ids_where(Search.buildings("#4 and not @1"))), {2})

if __name__ == '__main__':
    unittest.main()
