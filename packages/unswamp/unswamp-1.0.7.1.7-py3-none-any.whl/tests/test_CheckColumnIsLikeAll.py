from sys import path
path.append('../unswamp/')

from unittest import TestCase, main
from unswamp.checks.column import (
    CheckColumnLikeAll,
)
from helpers import TestHelpers


class TestCheckColumnLikeAll(TestCase):
    def test_CheckColumnLikeAll_properties(self):
        check_id = TestHelpers.str_random()
        col = TestHelpers.str_random()
        like = TestHelpers.str_random()
        check = CheckColumnLikeAll(check_id, col, like)

        TestHelpers.test_property(self, check, "id", check_id)
        TestHelpers.test_property(self, check, "column_name", col)
        TestHelpers.test_property(self, check, "like", like)

    def test_CheckColumnLikeAll_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        like = f"%{TestHelpers().same}%"
        check = CheckColumnLikeAll(check_id, col, like)
        dataset = TestHelpers.get_dataset()
        result = check.run(dataset)
        self.assertTrue(result.passed, f"Non expected check result for check '{type(check)}' with message '{result.message}'")

#TODO: test for serialization deserialization to compare properties

if __name__ == '__main__':
    main()
