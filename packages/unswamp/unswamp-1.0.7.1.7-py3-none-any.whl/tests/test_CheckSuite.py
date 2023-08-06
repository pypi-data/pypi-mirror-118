from unittest import TestCase, main
from unswamp.checks.column import (
    CheckColumnAllSame,
)
from unswamp.objects import (
    CheckSuite,
)
from helpers import TestHelpers
from sys import path
path.append('../unswamp/')


class TestCheckSuite(TestCase):
    def test_CheckSuite_properties(self):
        suite_id = TestHelpers.str_random()
        checks = ["newkey", "newvalue"]
        suite = CheckSuite(suite_id, checks)

        TestHelpers.test_property(self, suite, "id", suite_id)
        TestHelpers.test_property(self, suite, "checks", checks)

    def test_CheckSuite_run(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        val = TestHelpers.same
        check = CheckColumnAllSame(check_id, col, val)

        name = TestHelpers.str_random()
        checks = [check]
        suite = CheckSuite(name, checks)

        dataset = TestHelpers.get_dataset()
        check_run = suite.run(dataset)
        self.assertTrue(
            check_run.results[0].passed, f"Non expected check result for check '{type(check)}' with message '{check_run.results[0].message}'")

    def test_CheckSuite_serialization(self):
        check_id = TestHelpers.str_random()
        col = "Col_Same"
        val = TestHelpers.same
        check = CheckColumnAllSame(check_id, col, val)

        suite_id = TestHelpers.str_random()
        checks = [check]
        suite = CheckSuite(suite_id, checks)

        json_str = suite.to_json()
        suite2 = CheckSuite.from_json(json_str)
        TestHelpers.test_property(self, suite, "id", suite2.id)
        self.assertEqual(suite.checks[0].id, suite2.checks[0].id, f"unexpected deserialization result for type '{type(suite)}'")


if __name__ == '__main__':
    main()
