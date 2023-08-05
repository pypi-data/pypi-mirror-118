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
        def func(x): return x + x
        check = CheckColumnFunctionAll(check_id, col, val, func)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "column_value", val)
        TestHelpers.test_property(self, check, "column_function", func)

    def test_CheckColumnFunctionAll_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        val = TestHelpers.same
        func = Functions.check_column_equal
        check = CheckColumnFunctionAll(check_id, col, val, func)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(
            result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")


if __name__ == '__main__':
    main()
