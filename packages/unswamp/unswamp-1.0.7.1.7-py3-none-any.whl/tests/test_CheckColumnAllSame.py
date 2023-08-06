from sys import path
path.append('../unswamp/')

from helpers import TestHelpers
from unswamp.checks.column import (
    CheckColumnAllSame,
)
from unittest import TestCase, main



class TestCheckColumnAllSame(TestCase):
    def test_CheckColumnAllSame_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        val = TestHelpers.str_random()
        check = CheckColumnAllSame(check_id, col, val)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "column_value", val)

    def test_CheckColumnAllSame_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        val = TestHelpers.same
        check = CheckColumnAllSame(check_id, col, val)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(
            result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
