import string
from os import linesep
from io import StringIO
from datetime import datetime
import pandas as pd
from unswamp.checks import (
    Functions,
)

from random import seed, random, randint, choice, SystemRandom


class TestHelpers:
    curr_seed=42
    same="A"
    records=10
    datetime_format="%Y-%m-%d"
    regex_year = r"^[0-9]{4}$"
    function_name = "check_column_equal"

    @staticmethod
    def build_csv(records=100, curr_seed=42, same="A"):
        seed(curr_seed)
        csv = f"Col_Id,Col_Empty,Col_Same,Col_Year,Col_Gender,Col_Export{linesep}"
        for pos in range(records):
            year = randint(1901, datetime.today().year)
            gender = "M" if random() > 0.5 else "F"
            export = datetime.today().strftime(TestHelpers.datetime_format)
            csv += f"{pos},,{same},{year},{gender},{export}{linesep}"
        return csv

    @staticmethod
    def build_dataset(csv):
        data = StringIO(csv)
        dataset = pd.read_csv(data)
        return dataset

    @staticmethod
    def get_dataset():
        csv = TestHelpers.build_csv(TestHelpers.records, TestHelpers.curr_seed, TestHelpers.same)
        dataset = TestHelpers.build_dataset(csv)
        return dataset

    @staticmethod
    def str_random(length=10):
        rand = "".join(SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(length))
        return rand

    @staticmethod
    def test_property(test, obj, property, expectation):
        value = getattr(obj, property)
        test.assertEqual(value, expectation, f"Property '{property}' of object '{type(obj)}' should be '{expectation}' but was '{value}'!")
