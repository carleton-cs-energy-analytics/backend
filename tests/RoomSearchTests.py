import unittest
from backend.database.Search import Search
from backend.database.models import Rooms

string_beginning = " WHERE "


class RoomSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.rooms("@12"),
                         string_beginning + " buildings.building_id = 12;")

    def test_simple_tag(self):
        self.assertEqual(Search.rooms("#1"),
                         string_beginning + " (rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1);")

    def test_simple_room(self):
        self.assertEqual(Search.rooms("$12"),
                         string_beginning + " rooms.room_id = 12;")

    def test_simple_device(self):
        with self.assertRaises(Exception): Search.rooms("%12")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.rooms("*12")

    def test_simple_and(self):
        self.assertEqual(Search.rooms("and"),
                         string_beginning + " AND;")

    def test_simple_or(self):
        self.assertEqual(Search.rooms("or"),
                         string_beginning + " OR;")

    def test_simple_not(self):
        self.assertEqual(Search.rooms("not"),
                         string_beginning + " NOT;")

    def test_simple_floor(self):
        self.assertEqual(Search.rooms(":floor = 3"),
                         string_beginning + " rooms.floor = 3;")

    def test_simple_type(self):
        with self.assertRaises(Exception): Search.rooms(":type 4")

    def test_simple_unit(self):
        with self.assertRaises(Exception): Search.rooms(":unit 5")

    def test_simple_measurement(self):
        with self.assertRaises(Exception): Search.rooms(":measurement 'temperature'")

    def test_building_room(self):
        self.assertEquals(Search.rooms("@3 and $7"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 7;")

    def test_device_point(self):
        with self.assertRaises(Exception): Search.rooms("%310 or *78")

    def test_building_room_device(self):
        self.assertEquals(Search.rooms("@3 and $2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.room_id = 2;")

    def test_parenthesis_building_room_device(self):
        self.assertEquals(Search.rooms("(:floor = 2 or @3) and $2"),
                          string_beginning + "( rooms.floor = 2 OR buildings.building_id = 3) AND rooms.room_id = 2;")

    def test_nested_parenthesis_building_room_device(self):
        self.assertEquals(Search.rooms(":floor = 2 or (@3 or $2)"),
                          string_beginning + " rooms.floor = 2 OR( buildings.building_id = 3 OR rooms.room_id = 2);")

    def test_building_floor(self):
        self.assertEquals(Search.rooms("@3 and :floor > 2"),
                          string_beginning + " buildings.building_id = 3 AND rooms.floor > 2;")

    def test_search_building(self):
        ids = Rooms.ids_where(Search.rooms("@2"))
        self.assertEqual(set(ids), {4})

    def test_search_building_floor(self):
        ids = Rooms.ids_where(Search.rooms("@1 and :floor > 2"))
        self.assertEqual(ids, [1, 2])

    def test_search_building_or_device(self):
        with self.assertRaises(Exception): Rooms.ids_where(Search.rooms("@2 or %4"))

    def test_search_tag(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("#11"))), {1, 2, 3})

    def test_search_building_and_tag(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("@1 and #2"))), set())

    def test_search_tag_not_building(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("#7 and not @1"))), {4})

if __name__ == '__main__':
    unittest.main()
