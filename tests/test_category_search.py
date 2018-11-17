import unittest
from backend.database.Search import Search
from backend.database.models import Categories

class CategorySearchTests(unittest.TestCase):

    def test_all(self):
        self.assertEqual(Categories.all(), """[{"category_id":1,"category_name":"device_type"}, 
 {"category_id":2,"category_name":"building_usage_type"}, 
 {"category_id":3,"category_name":"room_type"}, 
 {"category_id":4,"category_name":"residence_occupancy_size"}, 
 {"category_id":5,"category_name":"department"}]""")

    def test_get_by_id_1(self):
        self.assertEqual(Categories.get_by_id(1), """{"category_id":1,"category_name":"device_type"}""")
