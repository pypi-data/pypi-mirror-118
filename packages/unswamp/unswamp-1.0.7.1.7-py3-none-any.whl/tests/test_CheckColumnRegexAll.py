from sys import path
path.append('../unswamp/')

from unittest import TestCase, main
from unswamp.checks.column import (
    CheckColumnRegexAll,
)
from helpers import TestHelpers


class TestCheckColumnRegexAll(TestCase):
    def test_CheckColumnRegexAll_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        regex = TestHelpers.str_random()
        check = CheckColumnRegexAll(check_id, col, regex)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "regex", regex)

    def test_CheckColumnRegexAll_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Year"
        regex = TestHelpers.regex_year
        check = CheckColumnRegexAll(check_id, col, regex)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
