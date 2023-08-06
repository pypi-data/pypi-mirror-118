from sys import path
path.append('../unswamp/')

from unittest import TestCase, main
from unswamp.checks.column import (
    CheckColumnIsNull,
)
from helpers import TestHelpers


class TestCheckColumnIsNull(TestCase):
    def test_CheckColumnIsNotNull_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        check = CheckColumnIsNull(check_id, col)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)

    def test_CheckColumnIsNull_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Empty"
        check = CheckColumnIsNull(check_id, col)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(
            result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
