import unittest
from backend.database.models import Tags


class TagTests(unittest.TestCase):

    def test_get_all(self):
        self.assertEqual(Tags.all(), """[{"tag_id":1,"tag_name":"thermostat","category_id":1,"category_name":"device_type","description":null}, 
 {"tag_id":2,"tag_name":"set","category_id":null,"category_name":null,"description":null}, 
 {"tag_id":3,"tag_name":"get","category_id":null,"category_name":null,"description":null}, 
 {"tag_id":4,"tag_name":"residential","category_id":2,"category_name":"building_usage_type","description":null}, 
 {"tag_id":5,"tag_name":"academic","category_id":2,"category_name":"building_usage_type","description":null}, 
 {"tag_id":6,"tag_name":"residence","category_id":3,"category_name":"room_type","description":null}, 
 {"tag_id":7,"tag_name":"single","category_id":4,"category_name":"residence_occupancy_size","description":null}, 
 {"tag_id":8,"tag_name":"room_temp","category_id":null,"category_name":null,"description":null}, 
 {"tag_id":9,"tag_name":"classroom","category_id":3,"category_name":"room_type","description":null}, 
 {"tag_id":10,"tag_name":"math_stats","category_id":5,"category_name":"department","description":null}, 
 {"tag_id":11,"tag_name":"computer_science","category_id":5,"category_name":"department","description":null}]""")

    def test_get_by_id(self):
        self.assertEqual(Tags.get_by_id(5),
                         """{"tag_id":5,"tag_name":"academic","category_id":2,"category_name":"building_usage_type","description":null}""")


if __name__ == '__main__':
    unittest.main()
