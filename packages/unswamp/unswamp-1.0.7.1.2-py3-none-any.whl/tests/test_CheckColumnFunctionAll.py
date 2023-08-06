from sys import path
path.append('../unswamp/')

from helpers import TestHelpers
from unswamp.checks import (
    CheckColumnFunctionAll,
    Functions,
)
from unittest import TestCase, main


class TestCheckColumnFunctionAll(TestCase):
    def test_CheckColumnFunctionAll_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        val = TestHelpers.str_random()
        # TODO: use mock
        func = TestHelpers.function_name
        check = CheckColumnFunctionAll(check_id, col, val, func)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "column_value", val)
        TestHelpers.test_property(self, check, "column_function_name", func)

    def test_CheckColumnFunctionAll_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        val = TestHelpers.same
        func = "check_column_equal"
        check = CheckColumnFunctionAll(check_id, col, val, func)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(
            result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
