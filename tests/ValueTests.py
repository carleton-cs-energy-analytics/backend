import unittest
from backend.database.models import Values, insert


class ValueTests(unittest.TestCase):

    @staticmethod
    def remove_point_to_be_added(attributes):
        insert("DELETE FROM values WHERE point_id = %s AND timestamp = %s AND int = %s", attributes)

    def test_get_add_single(self):
        point_id = (3,)
        timestamp = 23
        value = 8

        start_time = 9
        end_time = 80

        self.remove_point_to_be_added((point_id, start_time, end_time))

        Values.add(point_id, timestamp, value)
        result = Values.get(point_id, start_time, end_time)

        # silly fix because the value_id is changed each time the test is run
        self.assertEqual(result[:84] + result[-54:],
                         """[{"value_id":3,"point_name":"EV.RM107.RT","timestamp":13,"value":10}, 
 {"value_id":,"point_name":"EV.RM107.RT","timestamp":23,"value":8}]""")

        self.remove_point_to_be_added((point_id, start_time, end_time))

    def test_get_single(self):
        self.assertEqual(Values.get((1,), 0, 3),
                         '[{"value_id":1,"point_name":"CMC.328.RT","timestamp":2,"value":6}]')

    def test_get_many(self):
        self.assertEqual(Values.get((1, 3, 4, 5), 0, 13),
                         """[{"value_id":1,"point_name":"CMC.328.RT","timestamp":2,"value":6}, 
 {"value_id":2,"point_name":"EV.RM107.SP","timestamp":5,"value":9.8}, 
 {"value_id":3,"point_name":"EV.RM107.RT","timestamp":13,"value":10}]""")


if __name__ == '__main__':
    unittest.main()
