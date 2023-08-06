from sys import path
path.append('../unswamp/')

from unittest import TestCase, main
from unswamp.checks.column import (
    CheckColumnMatchStrftime,
)
from helpers import TestHelpers


class TestCheckColumnMatchStrftime(TestCase):
    def test_CheckColumnMatchStrftime_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        datetime_format = TestHelpers.str_random()
        check = CheckColumnMatchStrftime(check_id, col, datetime_format)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "datetime_format", datetime_format)

    def test_CheckColumnMatchStrftime_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Export"
        datetime_format = TestHelpers.datetime_format
        check = CheckColumnMatchStrftime(check_id, col, datetime_format)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
