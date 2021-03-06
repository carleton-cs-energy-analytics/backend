import unittest
from backend.database.Search import Search
from backend.database.models import Rooms


class RoomSearchTests(unittest.TestCase):

    def test_simple_building(self):
        self.assertEqual(Search.rooms("@12"), " buildings.building_id = 12")

    def test_simple_tag(self):
        self.assertEqual(Search.rooms("#1"),
                         " (rooms_tags.tag_id = 1 OR buildings_tags.tag_id = 1)")

    def test_simple_room(self):
        self.assertEqual(Search.rooms("$12"), " rooms.room_id = 12")

    def test_simple_device(self):
        with self.assertRaises(Exception): Search.rooms("%12")

    def test_simple_point(self):
        with self.assertRaises(Exception): Search.rooms("*12")

    def test_simple_and(self):
        self.assertEqual(Search.rooms("and"), " AND")

    def test_simple_or(self):
        self.assertEqual(Search.rooms("or"), " OR")

    def test_simple_not(self):
        self.assertEqual(Search.rooms("not"), " NOT")

    def test_simple_floor(self):
        self.assertEqual(Search.rooms(":floor = 3"), " rooms.floor = 3")

    def test_simple_type(self):
        with self.assertRaises(Exception): Search.rooms(":type 4")

    def test_simple_unit(self):
        with self.assertRaises(Exception): Search.rooms(":unit 5")

    def test_simple_measurement(self):
        with self.assertRaises(Exception): Search.rooms(":measurement 'temperature'")

    def test_building_room(self):
        self.assertEqual(Search.rooms("@3 and $7"),
                         " buildings.building_id = 3 AND rooms.room_id = 7")

    def test_device_point(self):
        with self.assertRaises(Exception): Search.rooms("%310 or *78")

    def test_building_room_device(self):
        self.assertEqual(Search.rooms("@3 and $2"),
                         " buildings.building_id = 3 AND rooms.room_id = 2")

    def test_parenthesis_building_room_device(self):
        self.assertEqual(Search.rooms("(:floor = 2 or @3) and $2"),
                         "( rooms.floor = 2 OR buildings.building_id = 3) AND rooms.room_id = 2")

    def test_nested_parenthesis_building_room_device(self):
        self.assertEqual(Search.rooms(":floor = 2 or (@3 or $2)"),
                         " rooms.floor = 2 OR( buildings.building_id = 3 OR rooms.room_id = 2)")

    def test_building_floor(self):
        self.assertEqual(Search.rooms("@3 and :floor > 2"),
                         " buildings.building_id = 3 AND rooms.floor > 2")

    # The following tests also test models.py

    def test_ids_where_building(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("@2"))), {4})

    def test_ids_where_building_floor(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("@1 and :floor > 2"))), {1, 2})

    def test_ids_where_building_or_device(self):
        with self.assertRaises(Exception): Rooms.ids_where(Search.rooms("@2 or %4"))

    def test_ids_where_tag(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("#11"))), {1, 2, 3})

    def test_ids_where_building_and_tag(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("@1 and #2"))), set())

    def test_ids_where_tag_not_building(self):
        self.assertEqual(set(Rooms.ids_where(Search.rooms("#7 and not @1"))), {4})

    def test_all(self):
        self.assertEqual(Rooms.all(), """[{"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","floor":3,"description":"Fishbowl","tags":["classroom","math_stats","academic","computer_science"]}, 
 {"room_id":2,"room_name":"304","building_id":1,"building_name":"CMC","floor":3,"description":null,"tags":["math_stats","academic","computer_science"]}, 
 {"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","floor":1,"description":null,"tags":["math_stats","academic","computer_science"]}, 
 {"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","floor":1,"description":null,"tags":["residential","residence","single"]}, 
 {"room_id":5,"room_name":"113","building_id":6,"building_name":"Sayles","floor":1,"description":"Sayles Great Space","tags":[]}]""")

    def test_where_building(self):
        self.assertEqual(Rooms.where(Search.rooms("@2")),
                         """[{"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","floor":1,"description":null,"tags":["residential","residence","single"]}]""")

    def test_where_building_floor(self):
        self.assertEqual(Rooms.where(Search.rooms("@1 and :floor > 2")), """[{"room_id":2,"room_name":"304","building_id":1,"building_name":"CMC","floor":3,"description":null,"tags":["math_stats","academic","computer_science"]}, 
 {"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","floor":3,"description":"Fishbowl","tags":["classroom","math_stats","academic","computer_science"]}]""")

    def test_where_building_or_device(self):
        with self.assertRaises(Exception): Rooms.where(Search.rooms("@2 or %4"))

    def test_where_tag(self):
        self.assertEqual(Rooms.where(Search.rooms("#11")), """[{"room_id":3,"room_name":"102","building_id":1,"building_name":"CMC","floor":1,"description":null,"tags":["math_stats","academic","computer_science"]}, 
 {"room_id":2,"room_name":"304","building_id":1,"building_name":"CMC","floor":3,"description":null,"tags":["math_stats","academic","computer_science"]}, 
 {"room_id":1,"room_name":"328","building_id":1,"building_name":"CMC","floor":3,"description":"Fishbowl","tags":["classroom","math_stats","academic","computer_science"]}]""")

    def test_where_building_and_tag(self):
        self.assertEqual(Rooms.where(Search.rooms("@1 and #2")), "[]")

    def test_where_tag_not_building(self):
        self.assertEqual(Rooms.where(Search.rooms("#7 and not @1")),
                         """[{"room_id":4,"room_name":"107","building_id":2,"building_name":"Evans","floor":1,"description":null,"tags":["residential","residence","single"]}]""")


if __name__ == '__main__':
    unittest.main()
