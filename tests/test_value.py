import unittest
from backend.database.models import Values, execute_and_commit


class ValueTests(unittest.TestCase):

    @staticmethod
    def remove_int_point_to_be_added(attributes):
        execute_and_commit("DELETE FROM values WHERE point_id = %s AND timestamp = %s AND int = %s",
                           attributes)

    @staticmethod
    def remove_double_point_to_be_added(attributes):
        execute_and_commit(
            "DELETE FROM values WHERE point_id = %s AND timestamp = %s AND double = %s",
            attributes)

    def test_add_get_single(self):
        point_name = ('EV.RM107.RT',)
        timestamp = 23
        value = 8

        start_time = 9
        end_time = 80

        self.remove_int_point_to_be_added(((3,), start_time, end_time))

        Values.add([(point_name, timestamp, value)])
        result = Values.get((3,), start_time, end_time)

        # silly fix because the value_id is changed each time the test is run
        self.assertEqual(result[:84] + result[-54:],
                         """[{"value_id":3,"point_name":"EV.RM107.RT","timestamp":13,"value":10}, 
 {"value_id":,"point_name":"EV.RM107.RT","timestamp":23,"value":8}]""")

        self.remove_int_point_to_be_added(((3,), timestamp, value))

    def test_add_enum(self):
        Values.add([('CMC.328.SP', 76, 'NRML')])
        self.remove_int_point_to_be_added(((2,), 76, 0))

    def test_add_many(self):
        Values.add([('CMC.328.SP', 90, 'FAULT'), ('EV.RM107.RT', 3, 8), ('EV.RM107.SP', 65, 77.8)])
        self.remove_int_point_to_be_added(((2,), 90, 1))
        self.remove_int_point_to_be_added(((3,), 3, 8))
        self.remove_double_point_to_be_added(((4,), 65, 77.8))

    def test_get_single(self):
        self.assertEqual(Values.get((1,), 0, 3),
                         '[{"value_id":1,"point_name":"CMC.328.RT","timestamp":2,"value":6}]')

    def test_get_many(self):
        self.assertEqual(Values.get((1, 3, 4, 5), 0, 13),
                         """[{"value_id":1,"point_name":"CMC.328.RT","timestamp":2,"value":6}, 
 {"value_id":3,"point_name":"EV.RM107.RT","timestamp":13,"value":10}, 
 {"value_id":2,"point_name":"EV.RM107.SP","timestamp":5,"value":9.8}]""")

    def test_get_enum(self):
        self.assertEqual(Values.get((2,), 0, 36),
                         """[{"value_id":4,"point_name":"CMC.328.SP","timestamp":35,"value":"FAULT"}]""")


if __name__ == '__main__':
    unittest.main()
